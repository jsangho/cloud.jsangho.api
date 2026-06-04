"""
PLE ?°ê¸° ? ì¤ì¼?´ì¤(interactor).

ple_router ??PleUseCase ??PleInteractor ??PleRepository(output port)
"""

from __future__ import annotations

from datetime import datetime, timezone

from core.matrix.oracle_database import LAYER_LOG
from kayfabe.app.ports.input.ple_schema import (
    BatchPredictionRequestSchema,
    BatchResultsRequestSchema,
    MatchResultSchema,
    MatchResultUpdateSchema,
    PleBoardSchema,
    PleEventSyncSchema,
    PredictionRequestSchema,
)
from kayfabe.app.ports.input.ple_use_case import PleUseCase
from kayfabe.app.ports.output.ple_repository import PleRepository
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository
from kayfabe.app.use_cases.pleinfo_interactor import PleInfoInteractor
from kayfabe.domain.entities.ple_model import PleEventStatus, PleMatchStatus
from kayfabe.domain.exceptions import PleAuthRequiredError

logger = LAYER_LOG

FINISHED_2026_RESULTS: dict[str, dict[str, MatchResultSchema]] = {
    "royal-rumble": {
        "rr26-gunther-styles": MatchResultSchema(winner_side="left", winner_name="Gunther"),
        "rr26-undisputed": MatchResultSchema(winner_side="left", winner_name="Drew McIntyre"),
        "rr26-women-rumble": MatchResultSchema(winner_index=1, winner_name="Liv Morgan"),
        "rr26-men-rumble": MatchResultSchema(winner_index=0, winner_name="Roman Reigns"),
    },
    "elimination-chamber": {
        "ec26-women": MatchResultSchema(winner_index=0, winner_name="Rhea Ripley"),
        "ec26-women-ic": MatchResultSchema(winner_side="left", winner_name="AJ Lee"),
        "ec26-whc": MatchResultSchema(winner_side="left", winner_name="CM Punk"),
        "ec26-men": MatchResultSchema(winner_index=0, winner_name="Randy Orton"),
    },
    "stand-and-deliver": {
        "sad26-preshow": MatchResultSchema(winner_side="left"),
        "sad26-sol-zaria": MatchResultSchema(winner_side="left", winner_name="Sol Ruca"),
        "sad26-women-na": MatchResultSchema(winner_side="left", winner_name="Tatum Paxley"),
        "sad26-na": MatchResultSchema(winner_side="left", winner_name="Myles Borne"),
        "sad26-tag": MatchResultSchema(winner_side="left", winner_name="The Vanity Project"),
        "sad26-women": MatchResultSchema(winner_index=0, winner_name="Lola Vice"),
        "sad26-nxt": MatchResultSchema(winner_index=0, winner_name="Tony D'Angelo"),
    },
    "wrestlemania": {
        "wm42-n1-six": MatchResultSchema(winner_side="left"),
        "wm42-n1-unsanctioned": MatchResultSchema(winner_side="left", winner_name="Jacob Fatu"),
        "wm42-n1-women-tag": MatchResultSchema(winner_index=0),
        "wm42-n1-women-ic": MatchResultSchema(winner_side="left", winner_name="Becky Lynch"),
        "wm42-n1-gunther-rollins": MatchResultSchema(winner_side="left", winner_name="Gunther"),
        "wm42-n1-women-world": MatchResultSchema(winner_side="left", winner_name="Liv Morgan"),
        "wm42-n1-undisputed": MatchResultSchema(winner_side="left", winner_name="Cody Rhodes"),
        "wm42-n2-femi-lesnar": MatchResultSchema(winner_side="left", winner_name="Oba Femi"),
        "wm42-n2-ic-ladder": MatchResultSchema(winner_index=0, winner_name="Penta"),
        "wm42-n2-us": MatchResultSchema(winner_side="left", winner_name="Trick Williams"),
        "wm42-n2-street": MatchResultSchema(winner_side="left", winner_name="Finn BÃ¡lor"),
        "wm42-n2-women": MatchResultSchema(winner_side="left", winner_name="Rhea Ripley"),
        "wm42-n2-whc": MatchResultSchema(winner_side="left", winner_name="Roman Reigns"),
    },
    "backlash": {
        "bl26-danhausen": MatchResultSchema(winner_side="left"),
        "bl26-iyo-asuka": MatchResultSchema(winner_side="left", winner_name="IYO SKY"),
        "bl26-us": MatchResultSchema(winner_side="left", winner_name="Trick Williams"),
        "bl26-breakker-rollins": MatchResultSchema(winner_side="left", winner_name="Bron Breakker"),
        "bl26-whc": MatchResultSchema(winner_side="left", winner_name="Roman Reigns"),
    },
}

FINISHED_2026_SLUGS = frozenset(FINISHED_2026_RESULTS.keys())


class PleInteractor(PleUseCase):
    """PLE ?°ê¸° ? ì¤ì¼?´ì¤ êµ¬íì²?"""

    def __init__(
        self,
        repository: PleRepository,
        info_repository: PleInfoRepository,
    ) -> None:
        self._repo = repository
        self._info = PleInfoInteractor(info_repository)

    async def _require_user(self, user_id: int) -> None:
        if not await self._repo.user_exists(user_id=user_id):
            raise PleAuthRequiredError("? í¨??ë¡ê·¸???ì???ë?ë¤.")

    async def sync_event(self, *, payload: PleEventSyncSchema) -> PleBoardSchema:
        logger.info(
            "[PleInteractor] sync_event -> Repository ??slug=%s matches=%d",
            payload.slug,
            len(payload.matches),
        )
        event = await self._repo.upsert_event_from_sync(payload)
        if payload.slug in FINISHED_2026_SLUGS:
            results = FINISHED_2026_RESULTS.get(payload.slug) or {}
            for match_key, result in results.items():
                await self._repo.set_match_result(
                    payload.slug, match_key, result, status=PleMatchStatus.FINISHED
                )

            if event.status != PleEventStatus.FINISHED:
                event.status = PleEventStatus.FINISHED
                event.finished_at = datetime.now(timezone.utc)
            await self._repo.flush()

        board = await self._info.get_board(slug=payload.slug)
        logger.info("[PleInteractor] sync_event <- Repository ??slug=%s", payload.slug)
        return board

    async def record_predictions_batch(
        self, *, slug: str, body: BatchPredictionRequestSchema
    ) -> PleBoardSchema:
        await self._require_user(body.user_id)
        event = await self._repo.get_event_by_slug(slug)
        if event is None:
            raise LookupError(slug)

        match_by_key = {m.match_key: m for m in event.matches}
        for item in body.predictions:
            row = match_by_key.get(item.match_key)
            if row is None:
                raise LookupError(item.match_key)
            if row.status == PleMatchStatus.FINISHED:
                raise ValueError(f"ì¢
ë£??ê²½ê¸°({item.match_key})?ë ?ì¸¡?????ìµ?ë¤.")
            await self._repo.upsert_prediction(row.id, body.client_id, item.pick, body.user_id)

        logger.info(
            "[PleInteractor] record_predictions_batch <- Repository ??slug=%s count=%d",
            slug,
            len(body.predictions),
        )
        return await self._info.get_board(slug=slug, client_id=body.client_id, user_id=body.user_id)

    async def set_match_results_batch(
        self, *, slug: str, body: BatchResultsRequestSchema
    ) -> PleBoardSchema:
        for item in body.results:
            result = MatchResultSchema(
                winner_side=item.winner_side,
                winner_index=item.winner_index,
                winner_name=item.winner_name,
            )
            row = await self._repo.set_match_result(slug, item.match_key, result, status=item.status)
            if row is None:
                raise LookupError(
                    f"ê²½ê¸° '{item.match_key}'ë¥?ì°¾ì ???ìµ?ë¤. PLE ì¹´ë ?ê¸°?????¤ì ?ë??ì£¼ì¸??"
                )

        logger.info(
            "[PleInteractor] set_match_results_batch <- Repository ??slug=%s count=%d",
            slug,
            len(body.results),
        )
        return await self._info.get_board(slug=slug)

    async def record_prediction(
        self, *, slug: str, match_key: str, body: PredictionRequestSchema
    ) -> PleBoardSchema:
        await self._require_user(body.user_id)
        event = await self._repo.get_event_by_slug(slug)
        if event is None:
            raise LookupError(slug)

        match = next((m for m in event.matches if m.match_key == match_key), None)
        if match is None:
            raise LookupError(match_key)
        if match.status == PleMatchStatus.FINISHED:
            raise ValueError("ì¢
ë£??ê²½ê¸°?ë ?ì¸¡?????ìµ?ë¤.")

        logger.info(
            "[PleInteractor] record_prediction -> Repository ??slug=%s match=%s userId=%s pick=%s",
            slug,
            match_key,
            body.user_id,
            body.pick,
        )
        await self._repo.upsert_prediction(match.id, body.client_id, body.pick, body.user_id)
        return await self._info.get_board(slug=slug, client_id=body.client_id, user_id=body.user_id)

    async def set_match_result(
        self, *, slug: str, match_key: str, body: MatchResultUpdateSchema
    ) -> PleBoardSchema:
        result = MatchResultSchema(
            winner_side=body.winner_side,
            winner_index=body.winner_index,
            winner_name=body.winner_name,
        )
        event = await self._repo.get_event_by_slug(slug)
        if event is None:
            raise LookupError(f"PLE '{slug}'ë¥?ì°¾ì ???ìµ?ë¤. ë¨¼ì? ì¹´ëë¥??ê¸°?í´ ì£¼ì¸??")

        row = await self._repo.set_match_result(slug, match_key, result, status=body.status)
        if row is None:
            raise LookupError(
                f"ê²½ê¸° '{match_key}'ë¥?ì°¾ì ???ìµ?ë¤. PLE ì¹´ë ?ê¸°?????¤ì ?ë??ì£¼ì¸??"
            )

        logger.info(
            "[PleInteractor] set_match_result <- Repository ??slug=%s match=%s",
            slug,
            match_key,
        )
        return await self._info.get_board(slug=slug)

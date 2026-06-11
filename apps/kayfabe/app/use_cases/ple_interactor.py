"""PLE 쓰기 유스케이스."""

from __future__ import annotations

from datetime import datetime, timezone

from kayfabe.app.dtos.ple_dto import (
    BatchPredictionCommand,
    BatchResultsCommand,
    MatchResultDto,
    MatchResultUpdateCommand,
    PleBoardDto,
    PleEventSyncCommand,
    PredictionCommand,
)
from kayfabe.app.exceptions import PleAuthRequiredError
from kayfabe.app.ports.input.ple import PleUseCase
from kayfabe.app.ports.output.ple_repository import PleRepository
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository
from kayfabe.app.use_cases.pleinfo_interactor import PleInfoInteractor
from kayfabe.domain.value_objects.ple_status_vo import PleEventStatus, PleMatchStatus

import logging

logger = logging.getLogger("uvicorn.error")

FINISHED_2026_RESULTS: dict[str, dict[str, MatchResultDto]] = {
    "royal-rumble": {
        "rr26-gunther-styles": MatchResultDto(winner_side="left", winner_name="Gunther"),
        "rr26-undisputed": MatchResultDto(winner_side="left", winner_name="Drew McIntyre"),
        "rr26-women-rumble": MatchResultDto(winner_index=1, winner_name="Liv Morgan"),
        "rr26-men-rumble": MatchResultDto(winner_index=0, winner_name="Roman Reigns"),
    },
    "elimination-chamber": {
        "ec26-women": MatchResultDto(winner_index=0, winner_name="Rhea Ripley"),
        "ec26-women-ic": MatchResultDto(winner_side="left", winner_name="AJ Lee"),
        "ec26-whc": MatchResultDto(winner_side="left", winner_name="CM Punk"),
        "ec26-men": MatchResultDto(winner_index=0, winner_name="Randy Orton"),
    },
    "stand-and-deliver": {
        "sad26-preshow": MatchResultDto(winner_side="left"),
        "sad26-sol-zaria": MatchResultDto(winner_side="left", winner_name="Sol Ruca"),
        "sad26-women-na": MatchResultDto(winner_side="left", winner_name="Tatum Paxley"),
        "sad26-na": MatchResultDto(winner_side="left", winner_name="Myles Borne"),
        "sad26-tag": MatchResultDto(winner_side="left", winner_name="The Vanity Project"),
        "sad26-women": MatchResultDto(winner_index=0, winner_name="Lola Vice"),
        "sad26-nxt": MatchResultDto(winner_index=0, winner_name="Tony D'Angelo"),
    },
    "wrestlemania": {
        "wm42-n1-six": MatchResultDto(winner_side="left"),
        "wm42-n1-unsanctioned": MatchResultDto(winner_side="left", winner_name="Jacob Fatu"),
        "wm42-n1-women-tag": MatchResultDto(winner_index=0),
        "wm42-n1-women-ic": MatchResultDto(winner_side="left", winner_name="Becky Lynch"),
        "wm42-n1-gunther-rollins": MatchResultDto(winner_side="left", winner_name="Gunther"),
        "wm42-n1-women-world": MatchResultDto(winner_side="left", winner_name="Liv Morgan"),
        "wm42-n1-undisputed": MatchResultDto(winner_side="left", winner_name="Cody Rhodes"),
        "wm42-n2-femi-lesnar": MatchResultDto(winner_side="left", winner_name="Oba Femi"),
        "wm42-n2-ic-ladder": MatchResultDto(winner_index=0, winner_name="Penta"),
        "wm42-n2-us": MatchResultDto(winner_side="left", winner_name="Trick Williams"),
        "wm42-n2-street": MatchResultDto(winner_side="left", winner_name="Finn Bálor"),
        "wm42-n2-women": MatchResultDto(winner_side="left", winner_name="Rhea Ripley"),
        "wm42-n2-whc": MatchResultDto(winner_side="left", winner_name="Roman Reigns"),
    },
    "backlash": {
        "bl26-danhausen": MatchResultDto(winner_side="left"),
        "bl26-iyo-asuka": MatchResultDto(winner_side="left", winner_name="IYO SKY"),
        "bl26-us": MatchResultDto(winner_side="left", winner_name="Trick Williams"),
        "bl26-breakker-rollins": MatchResultDto(winner_side="left", winner_name="Bron Breakker"),
        "bl26-whc": MatchResultDto(winner_side="left", winner_name="Roman Reigns"),
    },
}

FINISHED_2026_SLUGS = frozenset(FINISHED_2026_RESULTS.keys())


class PleInteractor(PleUseCase):
    def __init__(
        self,
        repository: PleRepository,
        info_repository: PleInfoRepository,
    ) -> None:
        self._repo = repository
        self._info = PleInfoInteractor(info_repository)

    async def _require_user(self, user_id: int) -> None:
        if not await self._repo.user_exists(user_id=user_id):
            raise PleAuthRequiredError("유효한 로그인 회원이 아닙니다.")

    async def sync_event(self, *, payload: PleEventSyncCommand) -> PleBoardDto:
        logger.info(
            "[PleInteractor] sync_event | slug=%s matches=%d",
            payload.slug,
            len(payload.matches),
        )
        snapshot = await self._repo.upsert_event_from_sync(payload)
        if payload.slug in FINISHED_2026_SLUGS:
            results = FINISHED_2026_RESULTS.get(payload.slug) or {}
            for match_key, result in results.items():
                await self._repo.set_match_result(
                    payload.slug,
                    match_key,
                    result,
                    status=PleMatchStatus.FINISHED,
                )

            if snapshot.status != PleEventStatus.FINISHED:
                await self._repo.mark_event_finished(
                    event_id=snapshot.id,
                    finished_at=datetime.now(timezone.utc),
                )
            await self._repo.flush()

        return await self._info.get_board(slug=payload.slug)

    async def record_predictions_batch(
        self, *, slug: str, body: BatchPredictionCommand
    ) -> PleBoardDto:
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
                raise ValueError(f"종료된 경기({item.match_key})에는 예측할 수 없습니다.")
            await self._repo.upsert_prediction(row.id, body.client_id, item.pick, body.user_id)

        logger.info(
            "[PleInteractor] record_predictions_batch | slug=%s count=%d",
            slug,
            len(body.predictions),
        )
        return await self._info.get_board(slug=slug, client_id=body.client_id, user_id=body.user_id)

    async def set_match_results_batch(
        self, *, slug: str, body: BatchResultsCommand
    ) -> PleBoardDto:
        for item in body.results:
            result = MatchResultDto(
                winner_side=item.winner_side,
                winner_index=item.winner_index,
                winner_name=item.winner_name,
            )
            ok = await self._repo.set_match_result(slug, item.match_key, result, status=item.status)
            if not ok:
                raise LookupError(
                    f"경기 '{item.match_key}'를 찾을 수 없습니다. PLE 카드 동기화를 다시 시도해 주세요."
                )
        logger.info(
            "[PleInteractor] set_match_results_batch | slug=%s count=%d",
            slug,
            len(body.results),
        )
        return await self._info.get_board(slug=slug)

    async def record_prediction(
        self, *, slug: str, match_key: str, body: PredictionCommand
    ) -> PleBoardDto:
        await self._require_user(body.user_id)
        event = await self._repo.get_event_by_slug(slug)
        if event is None:
            raise LookupError(slug)

        match = next((m for m in event.matches if m.match_key == match_key), None)
        if match is None:
            raise LookupError(match_key)
        if match.status == PleMatchStatus.FINISHED:
            raise ValueError("종료된 경기에는 예측할 수 없습니다.")

        logger.info(
            "[PleInteractor] record_prediction | slug=%s match=%s userId=%s pick=%s",
            slug,
            match_key,
            body.user_id,
            body.pick,
        )
        await self._repo.upsert_prediction(match.id, body.client_id, body.pick, body.user_id)
        return await self._info.get_board(slug=slug, client_id=body.client_id, user_id=body.user_id)

    async def set_match_result(
        self, *, slug: str, match_key: str, body: MatchResultUpdateCommand
    ) -> PleBoardDto:
        result = MatchResultDto(
            winner_side=body.winner_side,
            winner_index=body.winner_index,
            winner_name=body.winner_name,
        )
        event = await self._repo.get_event_by_slug(slug)
        if event is None:
            raise LookupError(f"PLE '{slug}'를 찾을 수 없습니다. 먼저 카드를 동기화해 주세요.")

        ok = await self._repo.set_match_result(slug, match_key, result, status=body.status)
        if not ok:
            raise LookupError(
                f"경기 '{match_key}'를 찾을 수 없습니다. PLE 카드 동기화를 다시 시도해 주세요."
            )
        logger.info("[PleInteractor] set_match_result | slug=%s match=%s", slug, match_key)
        return await self._info.get_board(slug=slug)

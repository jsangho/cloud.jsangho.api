"""
PLE 조회 유스케이스(interactor).

pleinfo_router → PleInfoUseCase → PleInfoInteractor → PleInfoRepository(output port)
"""

from __future__ import annotations

import json

from core.database import LAYER_LOG
from kayfabe.app.ports.input.ple_schema import (
    CompetitorSchema,
    MatchBoardSchema,
    MatchResultSchema,
    PleAiStatsSchema,
    PleBoardSchema,
    PleEventSummarySchema,
    VoteTotalsSchema,
)
from kayfabe.app.ports.input.pleinfo_use_case import PleInfoUseCase
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository

logger = LAYER_LOG


class PleInfoInteractor(PleInfoUseCase):
    """PLE 조회 유스케이스 구현체."""

    def __init__(self, repository: PleInfoRepository) -> None:
        self._repo = repository

    async def list_events(self) -> list[PleEventSummarySchema]:
        logger.info("[PleInfoInteractor] list_events -> Repository")
        events = await self._repo.list_events()
        rows = [
            PleEventSummarySchema(
                slug=e.slug,
                label=e.label,
                month=e.month,
                year=e.year,
                status=e.status,
                match_count=len(e.matches),
            )
            for e in events
        ]
        logger.info("[PleInfoInteractor] list_events <- Repository — count=%d", len(rows))
        return rows

    async def get_ai_stats(self) -> PleAiStatsSchema:
        logger.info("[PleInfoInteractor] get_ai_stats -> Repository")
        stats = await self._repo.get_ai_stats()
        logger.info("[PleInfoInteractor] get_ai_stats <- Repository")
        return stats

    async def get_board(
        self,
        *,
        slug: str,
        client_id: str | None = None,
        user_id: int | None = None,
    ) -> PleBoardSchema:
        logger.info(
            "[PleInfoInteractor] get_board -> Repository — slug=%s clientId=%s userId=%s",
            slug,
            client_id or "-",
            user_id if user_id is not None else "-",
        )
        event = await self._repo.get_event_by_slug(slug)
        if event is None:
            raise LookupError(slug)

        matches_out: list[MatchBoardSchema] = []
        for row in sorted(event.matches, key=lambda m: m.sort_order):
            card = json.loads(row.card_json)
            vote_raw, _ = self._repo.aggregate_votes(row)

            my_pick: str | None = None
            if user_id is not None:
                pred = await self._repo.get_prediction_by_user(row.id, user_id)
                if pred:
                    my_pick = pred.pick
            elif client_id:
                pred = await self._repo.get_prediction(row.id, client_id)
                if pred:
                    my_pick = pred.pick

            result = None
            if row.winner_pick or row.winner_name:
                if row.format == "multi":
                    try:
                        result = MatchResultSchema(
                            winner_index=int(row.winner_pick) if row.winner_pick else None,
                            winner_name=row.winner_name,
                        )
                    except ValueError:
                        result = MatchResultSchema(winner_name=row.winner_name)
                else:
                    result = MatchResultSchema(
                        winner_side=row.winner_pick if row.winner_pick in ("left", "right") else None,
                        winner_name=row.winner_name,
                    )

            matches_out.append(
                MatchBoardSchema(
                    id=row.match_key,
                    db_id=row.id,
                    title=row.title,
                    card_variant=row.card_variant,
                    format=row.format,
                    left=CompetitorSchema.model_validate(card["left"]) if card.get("left") else None,
                    right=CompetitorSchema.model_validate(card["right"]) if card.get("right") else None,
                    competitors=[CompetitorSchema.model_validate(c) for c in card.get("competitors") or []] or None,
                    bookmaker_decimal=card.get("bookmakerDecimal"),
                    status=row.status,
                    result=result,
                    site_votes=VoteTotalsSchema(
                        left=int(vote_raw.get("left", 0)),
                        right=int(vote_raw.get("right", 0)),
                        multi=list(vote_raw.get("multi") or []),
                    ),
                    locked=my_pick is not None,
                    my_pick=my_pick,
                    ai_pick=row.ai_pick,
                    ai_pick_name=row.ai_pick_name,
                    ai_correct=row.ai_correct,
                )
            )

        board = PleBoardSchema(
            slug=event.slug,
            label=event.label,
            month=event.month,
            year=event.year,
            status=event.status,
            finished_at=event.finished_at,
            matches=matches_out,
            updated_at=event.updated_at,
        )
        logger.info(
            "[PleInfoInteractor] get_board <- Repository — slug=%s matches=%d",
            slug,
            len(matches_out),
        )
        return board

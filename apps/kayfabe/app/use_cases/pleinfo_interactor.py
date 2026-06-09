"""PLE 조회 유스케이스."""

from __future__ import annotations

import json
import logging

from kayfabe.app.dtos.ple_dto import (
    CompetitorDto,
    MatchBoardDto,
    MatchResultDto,
    PleAiStatsDto,
    PleBoardDto,
    PleEventSummaryDto,
    VoteTotalsDto,
)
from kayfabe.app.ports.input.pleinfo_use_case import PleInfoUseCase
from kayfabe.app.ports.output.pleinfo_repository import PleInfoRepository

logger = logging.getLogger("uvicorn.error")


class PleInfoInteractor(PleInfoUseCase):
    def __init__(self, repository: PleInfoRepository) -> None:
        self._repo = repository

    async def list_events(self) -> list[PleEventSummaryDto]:
        logger.info("[PleInfoInteractor] list_events")
        events = await self._repo.list_events()
        return [
            PleEventSummaryDto(
                slug=e.slug,
                label=e.label,
                month=e.month,
                year=e.year,
                status=e.status,
                match_count=len(e.matches),
            )
            for e in events
        ]

    async def get_ai_stats(self) -> PleAiStatsDto:
        logger.info("[PleInfoInteractor] get_ai_stats")
        return await self._repo.get_ai_stats()

    async def get_board(
        self,
        *,
        slug: str,
        client_id: str | None = None,
        user_id: int | None = None,
    ) -> PleBoardDto:
        logger.info(
            "[PleInfoInteractor] get_board | slug=%s clientId=%s userId=%s",
            slug,
            client_id or "-",
            user_id if user_id is not None else "-",
        )
        event = await self._repo.get_event_by_slug(slug)
        if event is None:
            raise LookupError(slug)

        matches_out: list[MatchBoardDto] = []
        for row in event.matches:
            card = json.loads(row.card_json)
            vote_raw = await self._repo.aggregate_votes_for_match(
                match_id=row.id,
                fmt=row.format,
                card_json=row.card_json,
            )

            my_pick: str | None = None
            if user_id is not None:
                my_pick = await self._repo.get_prediction_pick_by_user(row.id, user_id)
            elif client_id:
                my_pick = await self._repo.get_prediction_pick(row.id, client_id)

            result = None
            if row.winner_pick or row.winner_name:
                if row.format == "multi":
                    try:
                        result = MatchResultDto(
                            winner_index=int(row.winner_pick) if row.winner_pick else None,
                            winner_name=row.winner_name,
                        )
                    except ValueError:
                        result = MatchResultDto(winner_name=row.winner_name)
                else:
                    result = MatchResultDto(
                        winner_side=row.winner_pick if row.winner_pick in ("left", "right") else None,
                        winner_name=row.winner_name,
                    )

            def _competitor(raw: dict | None) -> CompetitorDto | None:
                if not raw:
                    return None
                return CompetitorDto(
                    name=raw.get("name", ""),
                    is_champion=raw.get("isChampion"),
                )

            matches_out.append(
                MatchBoardDto(
                    id=row.match_key,
                    db_id=row.id,
                    title=row.title,
                    card_variant=row.card_variant,
                    format=row.format,
                    left=_competitor(card.get("left")),
                    right=_competitor(card.get("right")),
                    competitors=[
                        _competitor(c) for c in card.get("competitors") or []
                    ] or None,
                    bookmaker_decimal=card.get("bookmakerDecimal"),
                    status=row.status,
                    result=result,
                    site_votes=VoteTotalsDto(
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

        return PleBoardDto(
            slug=event.slug,
            label=event.label,
            month=event.month,
            year=event.year,
            status=event.status,
            finished_at=event.finished_at,
            matches=matches_out,
            updated_at=event.updated_at,
        )

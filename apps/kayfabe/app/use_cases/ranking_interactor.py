from __future__ import annotations

import logging

from kayfabe.app.dtos.ranking_dto import LeaderboardRow, RankingRowDto, RankingsDto
from kayfabe.app.ports.input.ranking import RankingUseCase
from kayfabe.app.ports.output.ple_repository import PleRepository
from kayfabe.app.ports.output.ranking_repository import RankingRepository

logger = logging.getLogger("uvicorn.error")


class RankingInteractor(RankingUseCase):
    def __init__(
        self,
        *,
        ranking_repository: RankingRepository,
        ple_repository: PleRepository,
    ) -> None:
        self._ranking_repository = ranking_repository
        self._ple_repository = ple_repository

    @staticmethod
    def _to_row_dto(row: LeaderboardRow) -> RankingRowDto:
        graded = row.graded
        accuracy = (row.correct / graded) if graded > 0 else 0.0
        return RankingRowDto(
            rank=row.rank,
            nickname=row.nickname,
            score=row.score,
            accuracy=round(accuracy, 4),
        )

    async def list_rankings(
        self,
        *,
        limit: int = 120,
        nickname: str | None = None,
    ) -> RankingsDto:
        logger.info(
            "[RankingInteractor] list_rankings | limit=%d nickname=%s",
            limit,
            nickname or "-",
        )
        capped = min(max(limit, 1), 500)
        await self._ple_repository.refresh_all_match_point_values()
        raw_rows = await self._ranking_repository.list_ranked(capped)
        rows = [self._to_row_dto(r) for r in raw_rows]

        my_rank: RankingRowDto | None = None
        if nickname:
            my_rank = next((r for r in rows if r.nickname == nickname), None)
            if my_rank is None:
                mine = await self._ranking_repository.get_ranked_by_nickname(nickname)
                if mine is not None:
                    my_rank = self._to_row_dto(mine)

        logger.info("[RankingInteractor] list_rankings | rows=%d", len(rows))
        return RankingsDto(rows=rows, my_rank=my_rank)

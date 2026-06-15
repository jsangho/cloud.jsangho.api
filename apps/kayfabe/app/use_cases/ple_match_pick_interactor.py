"""PLE 예측 순위 유스케이스."""

from __future__ import annotations

import logging

from kayfabe.app.dtos.myself_dto import MyselfQuery, MyselfRepository, MyselfResponse, MyselfUseCase
from kayfabe.app.dtos.ranking_dto import LeaderboardRow, RankingRowResponse, RankingsResponse
from kayfabe.app.ports.input.ple_match_pick_use_case import RankingUseCase
from kayfabe.app.ports.output.ple_events_repository import PleRepository
from kayfabe.app.ports.output.ple_match_pick_repository import RankingRepository

logger = logging.getLogger("uvicorn.error")


class PleMatchPickInteractor(RankingUseCase):
    def __init__(
        self,
        *,
        ranking_repository: RankingRepository,
        ple_repository: PleRepository,
    ) -> None:
        self._ranking_repository = ranking_repository
        self._ple_repository = ple_repository

    @staticmethod
    def _to_row_dto(row: LeaderboardRow) -> RankingRowResponse:
        graded = row.graded
        accuracy = (row.correct / graded) if graded > 0 else 0.0
        return RankingRowResponse(
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
    ) -> RankingsResponse:
        logger.info(
            "[RankingInteractor] list_rankings | limit=%d nickname=%s",
            limit,
            nickname or "-",
        )
        capped = min(max(limit, 1), 500)
        await self._ple_repository.refresh_all_match_point_values()
        raw_rows = await self._ranking_repository.list_ranked(capped)
        rows = [self._to_row_dto(r) for r in raw_rows]

        my_rank: RankingRowResponse | None = None
        if nickname:
            my_rank = next((r for r in rows if r.nickname == nickname), None)
            if my_rank is None:
                mine = await self._ranking_repository.get_ranked_by_nickname(nickname)
                if mine is not None:
                    my_rank = self._to_row_dto(mine)

        logger.info("[RankingInteractor] list_rankings | rows=%d", len(rows))
        return RankingsResponse(rows=rows, my_rank=my_rank)


RankingInteractor = PleMatchPickInteractor


class RankingMyselfInteractor(MyselfUseCase):
    def __init__(self, repository: MyselfRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, query: MyselfQuery) -> MyselfResponse:
        return await self.repository.introduce_myself(query)

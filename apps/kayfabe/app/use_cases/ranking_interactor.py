from __future__ import annotations

from core.matrix.oracle_database import LAYER_LOG
from kayfabe.adapter.inbound.api.schemas.ranking_schema import RankingRowSchema, RankingsResponseSchema
from kayfabe.app.dtos.ranking_dto import LeaderboardRow
from kayfabe.app.ports.input.ranking_use_case import RankingUseCase
from kayfabe.app.ports.output.ple_repository import PleRepository
from kayfabe.app.ports.output.ranking_repository import RankingRepository

logger = LAYER_LOG


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
    def _to_schema(row: LeaderboardRow) -> RankingRowSchema:
        graded = row.graded
        accuracy = (row.correct / graded) if graded > 0 else 0.0
        return RankingRowSchema(
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
    ) -> RankingsResponseSchema:
        logger.info(
            "[RankingInteractor] list_rankings -> Repository limit=%d nickname=%s",
            limit,
            nickname or "-",
        )
        capped = min(max(limit, 1), 500)
        await self._ple_repository.refresh_all_match_point_values()
        raw_rows = await self._ranking_repository.list_ranked(capped)
        rows = [self._to_schema(r) for r in raw_rows]

        my_rank: RankingRowSchema | None = None
        if nickname:
            my_rank = next((r for r in rows if r.nickname == nickname), None)
            if my_rank is None:
                mine = await self._ranking_repository.get_ranked_by_nickname(nickname)
                if mine is not None:
                    my_rank = self._to_schema(mine)

        logger.info("[RankingInteractor] list_rankings <- Repository rows=%d", len(rows))
        return RankingsResponseSchema(rows=rows, my_rank=my_rank)

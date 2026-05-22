from sqlalchemy.ext.asyncio import AsyncSession

from database import LAYER_LOG
from kayfabe.app.repositories.ple_repository import PleRepository
from kayfabe.app.repositories.ranking_repository import LeaderboardRow, RankingRepository
from kayfabe.app.schemas.ranking_schema import RankingRowSchema, RankingsResponseSchema

logger = LAYER_LOG


class RankingService:
    def __init__(self, db: AsyncSession) -> None:
        self.ranking_repository = RankingRepository(db)
        self.ple_repository = PleRepository(db)

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
            "[RankingService] list_rankings -> Repository — limit=%d nickname=%s",
            limit,
            nickname or "-",
        )
        capped = min(max(limit, 1), 500)
        await self.ple_repository.refresh_all_match_point_values()
        raw_rows = await self.ranking_repository.list_ranked(capped)
        rows = [self._to_schema(r) for r in raw_rows]

        my_rank: RankingRowSchema | None = None
        if nickname:
            my_rank = next((r for r in rows if r.nickname == nickname), None)
            if my_rank is None:
                mine = await self.ranking_repository.get_ranked_by_nickname(nickname)
                if mine is not None:
                    my_rank = self._to_schema(mine)

        logger.info("[RankingService] list_rankings <- Repository — rows=%d", len(rows))
        return RankingsResponseSchema(rows=rows, my_rank=my_rank)

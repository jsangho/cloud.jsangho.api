from sqlalchemy.ext.asyncio import AsyncSession

from database import LAYER_LOG
from kayfabe.app.schemas.ranking_schema import RankingsResponseSchema
from kayfabe.app.services.ranking_service import RankingService

logger = LAYER_LOG


class RankingController:
    def __init__(self, db: AsyncSession) -> None:
        self.ranking_service = RankingService(db)

    async def list_rankings(
        self,
        *,
        limit: int = 120,
        nickname: str | None = None,
    ) -> RankingsResponseSchema:
        logger.info("[RankingController] list_rankings -> Service")
        return await self.ranking_service.list_rankings(limit=limit, nickname=nickname)

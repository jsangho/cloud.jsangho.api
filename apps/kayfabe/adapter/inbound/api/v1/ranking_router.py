from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from kayfabe.app.ports.input.ranking_schema import RankingsResponseSchema
from kayfabe.app.use_cases.ranking_interactor import RankingService


router = APIRouter(prefix="/ple/ranking", tags=["ranking"])


def get_ranking_service(db: AsyncSession = Depends(get_db)) -> RankingService:
    return RankingService(db)


@router.get(
    "/rankings",
    response_model=RankingsResponseSchema,
    response_model_by_alias=True,
)
async def list_rankings(
    limit: int = 120,
    nickname: str | None = None,
    service: RankingService = Depends(get_ranking_service),
):
    """
    PLE ?¹ë??ì¸¡ ?ì (?ìÂ·?ì¤ë¥?.
    ê²½ê¸° ê²°ê³¼(ple_matches.winner_pick) ?ì  ??pick ?¼ì¹ë¶ì´ ?ë ì§ê³?©ë??
    nickname ì¿¼ë¦¬ë¡????ì(myRank)ë¥??¨ê» ì¡°í?????ìµ?ë¤.
    """
    return await service.list_rankings(limit=limit, nickname=nickname)


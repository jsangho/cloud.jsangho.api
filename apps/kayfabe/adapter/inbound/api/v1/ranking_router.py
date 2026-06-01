from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
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
    PLE 승부예측 순위 (점수·적중률).
    경기 결과(ple_matches.winner_pick) 확정 시 pick 일치분이 자동 집계됩니다.
    nickname 쿼리로 내 순위(myRank)를 함께 조회할 수 있습니다.
    """
    return await service.list_rankings(limit=limit, nickname=nickname)


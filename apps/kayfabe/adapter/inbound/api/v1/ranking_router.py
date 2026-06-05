from __future__ import annotations

from fastapi import APIRouter, Depends

from kayfabe.adapter.inbound.api.schemas.ranking_schema import RankingsResponseSchema
from kayfabe.app.ports.input.ranking_use_case import RankingUseCase
from kayfabe.dependencies.ranking import get_ranking_use_case


ranking_router = APIRouter(tags=["ranking"])


@ranking_router.get(
    "/rankings",
    response_model=RankingsResponseSchema,
    response_model_by_alias=True,
)
async def list_rankings(
    limit: int = 120,
    nickname: str | None = None,
    use_case: RankingUseCase = Depends(get_ranking_use_case),
):
    """
    PLE 예측 순위 (점수·적중률).
    경기 결과(ple_matches.winner_pick) 확정 시 pick 일치분이 자동 집계됩니다.
    nickname 쿼리로 내 순위(myRank)를 함께 조회할 수 있습니다.
    """
    return await use_case.list_rankings(limit=limit, nickname=nickname)

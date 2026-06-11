from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from kayfabe.adapter.outbound.mappers.ranking_schema_mapper import rankings_to_schema
from kayfabe.adapter.inbound.api.schemas.ranking_schema import RankingsResponseSchema
from kayfabe.app.ports.input.ranking import RankingUseCase
from kayfabe.dependencies.ranking_provider import get_ranking

logger = logging.getLogger("uvicorn.error")

ranking_router = APIRouter(tags=["ranking"])


@ranking_router.get(
    "/rankings",
    response_model=RankingsResponseSchema,
    response_model_by_alias=True,
)
async def list_rankings(
    limit: int = 120,
    nickname: str | None = None,
    use_case: RankingUseCase = Depends(get_ranking),
):
    logger.info("[RankingRouter] list_rankings | limit=%d nickname=%s", limit, nickname or "-")
    return rankings_to_schema(await use_case.list_rankings(limit=limit, nickname=nickname))

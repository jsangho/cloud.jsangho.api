from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from kayfabe.adapter.inbound.api.schemas.championship_schema import (
    ChampionshipBoardResponseSchema,
)
from kayfabe.app.ports.input.championship import ChampionshipUseCase
from kayfabe.dependencies.championship_provider import get_championship

logger = logging.getLogger("uvicorn.error")

championship_router = APIRouter(prefix="/championship", tags=["championship"])


@championship_router.get(
    "",
    response_model=ChampionshipBoardResponseSchema,
    response_model_by_alias=True,
)
async def get_championship_board(
    use_case: ChampionshipUseCase = Depends(get_championship),
):
    """브랜드별 현역 WWE 챔피언 (메인·2선·태그·기타)."""
    logger.info("[ChampionshipRouter] get_championship_board")
    return (await use_case.get_board()).to_schema()

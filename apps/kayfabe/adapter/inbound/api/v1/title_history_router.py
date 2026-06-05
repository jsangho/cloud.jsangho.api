from __future__ import annotations

from fastapi import APIRouter, Depends

from kayfabe.adapter.inbound.api.schemas.title_history_schema import (
    CompetitorTitleHistoryResponseSchema,
)
from kayfabe.app.ports.input.title_history_use_case import TitleHistoryUseCase
from kayfabe.dependencies.title_history import get_title_history_use_case


title_history_router = APIRouter(prefix="/title-history", tags=["title-history"])


@title_history_router.get(
    "/competitors/{name}",
    response_model=CompetitorTitleHistoryResponseSchema,
    response_model_by_alias=True,
)
async def get_competitor_title_history(
    name: str,
    use_case: TitleHistoryUseCase = Depends(get_title_history_use_case),
):
    """선수/팀의 실제 WWE 챔피언십 벨트 획득 이력 (NeonDB)."""
    return await use_case.get_competitor_title_history(name)


@title_history_router.post("/sync")
async def sync_title_history_from_catalog(
    use_case: TitleHistoryUseCase = Depends(get_title_history_use_case),
):
    """실제 WWE 타이틀 획득 카탈로그로 NeonDB를 재생성."""
    count = await use_case.sync_from_real_catalog()
    return {"synced": count}

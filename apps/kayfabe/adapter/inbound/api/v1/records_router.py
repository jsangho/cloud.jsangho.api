from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from kayfabe.adapter.inbound.api.schemas.records_schema import (
    CompetitorListResponseSchema,
    CompetitorProfileResponseSchema,
)
from kayfabe.app.ports.input.records_use_case import RecordsUseCase
from kayfabe.dependencies.records import get_records_use_case


records_router = APIRouter(prefix="/records", tags=["records"])


@records_router.get(
    "/competitors",
    response_model=CompetitorListResponseSchema,
    response_model_by_alias=True,
)
async def list_competitors(
    q: str | None = None,
    use_case: RecordsUseCase = Depends(get_records_use_case),
):
    """PLE 출전 선수 목록 (Neon 동기화 카드 기준). `q`로 이름 검색."""
    return await use_case.list_competitors(q=q)


@records_router.get(
    "/competitors/{name}",
    response_model=CompetitorProfileResponseSchema,
    response_model_by_alias=True,
)
async def get_competitor_profile(
    name: str,
    use_case: RecordsUseCase = Depends(get_records_use_case),
):
    """선수별 PLE 승패 기록."""
    profile = await use_case.get_competitor_profile(name)
    if not profile.matches and not await _competitor_exists(use_case, name):
        raise HTTPException(status_code=404, detail="선수를 찾을 수 없습니다.")
    return profile


async def _competitor_exists(use_case: RecordsUseCase, name: str) -> bool:
    listed = await use_case.list_competitors()
    target = name.strip().lower()
    return any(n.lower() == target for n in listed.names)

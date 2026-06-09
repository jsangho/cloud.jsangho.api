from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException

from kayfabe.adapter.inbound.api.schemas.records_schema import (
    CompetitorListResponseSchema,
    CompetitorProfileResponseSchema,
)
from kayfabe.app.ports.input.records_use_case import RecordsUseCase
from kayfabe.dependencies.records_provider import get_records_use_case

logger = logging.getLogger("uvicorn.error")

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
    logger.info("[RecordsRouter] list_competitors | q=%s", q or "-")
    return (await use_case.list_competitors(q=q)).to_schema()


@records_router.get(
    "/competitors/{name}",
    response_model=CompetitorProfileResponseSchema,
    response_model_by_alias=True,
)
async def get_competitor_profile(
    name: str,
    use_case: RecordsUseCase = Depends(get_records_use_case),
):
    logger.info("[RecordsRouter] get_competitor_profile | name=%s", name)
    profile = await use_case.get_competitor_profile(name)
    if not profile.matches and not await _competitor_exists(use_case, name):
        raise HTTPException(status_code=404, detail="선수를 찾을 수 없습니다.")
    return profile.to_schema()


async def _competitor_exists(use_case: RecordsUseCase, name: str) -> bool:
    listed = await use_case.list_competitors()
    target = name.strip().lower()
    return any(n.lower() == target for n in listed.names)

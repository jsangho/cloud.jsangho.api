from __future__ import annotations

from fastapi import APIRouter, Depends

from kayfabe.adapter.inbound.api.schemas.result_schema import PleResultsResponse
from kayfabe.app.ports.input.result_use_case import ResultUseCase
from kayfabe.dependencies.result import get_result_use_case


result_router = APIRouter(prefix="/ple/results", tags=["results"])


@result_router.get("/results", response_model=PleResultsResponse)
async def list_ple_results(
    year: int = 2026,
    use_case: ResultUseCase = Depends(get_result_use_case),
):
    return await use_case.list_results(year)

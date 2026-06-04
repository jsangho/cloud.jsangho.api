from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from kayfabe.adapter.outbound.pg.result_pg_repository import ResultRepository
from kayfabe.app.ports.input.result_schema import PleResultsResponse
from kayfabe.app.use_cases.result_interactor import ResultService


router = APIRouter(prefix="/ple/results", tags=["results"])


def get_result_service(db: AsyncSession = Depends(get_db)) -> ResultService:
    return ResultService(ResultRepository(db))


@router.get("/results", response_model=PleResultsResponse)
async def list_ple_results(
    year: int = 2026,
    service: ResultService = Depends(get_result_service),
):
    return await service.list_results(year)


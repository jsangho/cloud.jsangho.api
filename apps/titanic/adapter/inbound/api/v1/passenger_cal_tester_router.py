from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase

cal_tester_router = APIRouter(prefix="/cal", tags=["cal"])


def get_cal_tester_use_case(db: AsyncSession = Depends(get_db)) -> CalTesterUseCase:
    from titanic.adapter.outbound.pg.passenger_cal_tester_pg_repository import CalTesterPgRepository
    from titanic.app.use_cases.passenger_cal_tester_interactor import CalTesterInteractor

    return CalTesterInteractor(CalTesterPgRepository(db))


@cal_tester_router.get("/pistol")
async def get_cal_tester(
    use_case: CalTesterUseCase = Depends(get_cal_tester_use_case),
):
    return await use_case.get_tester()

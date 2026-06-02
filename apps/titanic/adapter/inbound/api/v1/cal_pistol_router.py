from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.app.ports.input.cal_pistol_use_case import CalPistolUseCase

cal_pistol_router = APIRouter(prefix="/cal", tags=["cal"])


def get_cal_pistol_use_case(db: AsyncSession = Depends(get_db)) -> CalPistolUseCase:
    from titanic.adapter.outbound.pg.cal_pistol_pg_repository import CalPistolPgRepository
    from titanic.app.use_cases.cal_pistol_interactor import CalPistolInteractor

    return CalPistolInteractor(CalPistolPgRepository(db))


@cal_pistol_router.get("/pistol")
async def get_cal_pistol(
    use_case: CalPistolUseCase = Depends(get_cal_pistol_use_case),
):
    return await use_case.get_pistol()

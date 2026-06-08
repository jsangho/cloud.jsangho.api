from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase

isidor_couple_router = APIRouter(prefix="/isidor", tags=["isidor"])


def get_isidor_couple_use_case(db: AsyncSession = Depends(get_db)) -> IsidorCoupleUseCase:
    from titanic.adapter.outbound.pg.passenger_isidor_couple_pg_repository import IsidorCouplePgRepository
    from titanic.app.use_cases.passenger_isidor_couple_interactor import IsidorCoupleInteractor

    return IsidorCoupleInteractor(IsidorCouplePgRepository(db))


@isidor_couple_router.get("/bed")
async def get_isidor_couple(
    use_case: IsidorCoupleUseCase = Depends(get_isidor_couple_use_case),
):
    return await use_case.get_couple()

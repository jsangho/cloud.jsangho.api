from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase

molly_scaler_router = APIRouter(prefix="/molly", tags=["molly"])


def get_molly_scaler_use_case(db: AsyncSession = Depends(get_db)) -> MollyScalerUseCase:
    from titanic.adapter.outbound.pg.passenger_molly_scaler_pg_repository import MollyScalerPgRepository
    from titanic.app.use_cases.passenger_molly_scaler_interactor import MollyScalerInteractor

    return MollyScalerInteractor(MollyScalerPgRepository(db))


@molly_scaler_router.get("/scaler")
async def get_molly_scaler(
    use_case: MollyScalerUseCase = Depends(get_molly_scaler_use_case),
):
    return await use_case.get_scaler()

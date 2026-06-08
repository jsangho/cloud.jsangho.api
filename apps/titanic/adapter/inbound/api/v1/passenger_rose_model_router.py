from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase

rose_model_router = APIRouter(prefix="/rose", tags=["rose"])


def get_rose_model_use_case(db: AsyncSession = Depends(get_db)) -> RoseModelUseCase:
    from titanic.adapter.outbound.pg.passenger_rose_model_pg_repository import RoseModelPgRepository
    from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor

    return RoseModelInteractor(RoseModelPgRepository(db))


@rose_model_router.get("/diamond")
async def get_rose_model(
    use_case: RoseModelUseCase = Depends(get_rose_model_use_case),
):
    return await use_case.get_model()

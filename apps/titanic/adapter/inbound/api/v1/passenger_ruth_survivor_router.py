from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_ruth_survivor_use_case import RuthSurvivorUseCase

ruth_survivor_router = APIRouter(prefix="/ruth", tags=["ruth"])


def get_ruth_survivor_use_case(db: AsyncSession = Depends(get_db)) -> RuthSurvivorUseCase:
    from titanic.adapter.outbound.pg.passenger_ruth_survivor_pg_repository import RuthSurvivorPgRepository
    from titanic.app.use_cases.passenger_ruth_survivor_interactor import RuthSurvivorInteractor

    return RuthSurvivorInteractor(RuthSurvivorPgRepository(db))


@ruth_survivor_router.get("/corset")
async def get_ruth_survivor(
    use_case: RuthSurvivorUseCase = Depends(get_ruth_survivor_use_case),
):
    return await use_case.get_survivor()

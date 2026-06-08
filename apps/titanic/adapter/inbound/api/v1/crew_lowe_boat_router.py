from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase

lowe_boat_router = APIRouter(prefix="/lowe", tags=["lowe"])


def get_lowe_boat_use_case(
    db: AsyncSession = Depends(get_db),
) -> LoweBoatUseCase:
    from titanic.adapter.outbound.pg.crew_lowe_boat_pg_repository import (
        LoweBoatPgRepository,
    )
    from titanic.app.use_cases.crew_lowe_boat_interactor import LoweBoatInteractor

    return LoweBoatInteractor(LoweBoatPgRepository(db))


@lowe_boat_router.get("/boat")
async def get_lowe_boat(
    use_case: LoweBoatUseCase = Depends(get_lowe_boat_use_case),
):
    return await use_case.get_boat()

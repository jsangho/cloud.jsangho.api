from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.dependencies.crew_lowe_boat_provider import get_lowe_boat_use_case

lowe_boat_router = APIRouter(prefix="/lowe", tags=["lowe"])


@lowe_boat_router.get("/boat")
async def get_lowe_boat(
    use_case: LoweBoatUseCase = Depends(get_lowe_boat_use_case),
):
    return await use_case.get_boat()

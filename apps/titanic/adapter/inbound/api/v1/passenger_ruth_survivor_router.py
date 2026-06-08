from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_ruth_survivor_use_case import RuthSurvivorUseCase
from titanic.dependencies.passenger_ruth_survivor_provider import get_ruth_survivor_use_case

ruth_survivor_router = APIRouter(prefix="/ruth", tags=["ruth"])


@ruth_survivor_router.get("/survivor")
async def get_ruth_survivor(
    use_case: RuthSurvivorUseCase = Depends(get_ruth_survivor_use_case),
):
    return await use_case.get_survivor()

from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.dependencies.passenger_isidor_couple_provider import get_isidor_couple_use_case

isidor_couple_router = APIRouter(prefix="/isidor", tags=["isidor"])


@isidor_couple_router.get("/couple")
async def get_isidor_couple(
    use_case: IsidorCoupleUseCase = Depends(get_isidor_couple_use_case),
):
    return await use_case.get_couple()

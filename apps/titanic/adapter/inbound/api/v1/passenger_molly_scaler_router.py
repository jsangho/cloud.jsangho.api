from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.dependencies.passenger_molly_scaler_provider import get_molly_scaler_use_case

molly_scaler_router = APIRouter(prefix="/molly", tags=["molly"])


@molly_scaler_router.get("/scaler")
async def get_molly_scaler(
    use_case: MollyScalerUseCase = Depends(get_molly_scaler_use_case),
):
    return await use_case.get_scaler()

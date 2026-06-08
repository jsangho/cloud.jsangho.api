from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case

rose_model_router = APIRouter(prefix="/rose", tags=["rose"])


@rose_model_router.get("/model")
async def get_rose_model(
    use_case: RoseModelUseCase = Depends(get_rose_model_use_case),
):
    return await use_case.get_model()

from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case

jack_trainer_router = APIRouter(prefix="/jack", tags=["jack"])


@jack_trainer_router.get("/trainer")
async def get_jack_trainer(
    use_case: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
):
    return await use_case.get_trainer()

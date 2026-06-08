from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase

jack_trainer_router = APIRouter(prefix="/jack", tags=["jack"])


def get_jack_trainer_use_case(db: AsyncSession = Depends(get_db)) -> JackTrainerUseCase:
    from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainerPgRepository
    from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor

    return JackTrainerInteractor(JackTrainerPgRepository(db))


@jack_trainer_router.get("/sketch")
async def get_jack_trainer(
    use_case: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
):
    return await use_case.get_trainer()

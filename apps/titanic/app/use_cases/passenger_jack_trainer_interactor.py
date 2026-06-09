from __future__ import annotations

import logging

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger("uvicorn.error")


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        logger.info("[JackTrainerUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        return await self.repository.introduce_myself(query)

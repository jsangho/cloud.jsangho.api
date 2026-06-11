from __future__ import annotations
from fastapi import Depends
import logging
from collections.abc import Iterator

from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer
from titanic.dependencies.passenger_rose_model_provider import get_rose_model
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema
from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository


logger = logging.getLogger("uvicorn.error")


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def chat(self, schema: ChatSchema,
        jack: JackTrainerUseCase = Depends(get_jack_trainer),
        rose: RoseModelUseCase = Depends(get_rose_model),
        ) -> SmithCaptainResponse:
        return await self.repository.chat(schema.message)

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        logger.info("[SmithCaptainUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        return await self.repository.introduce_myself(query)

    
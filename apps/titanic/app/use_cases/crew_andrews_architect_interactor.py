from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository

logger = logging.getLogger("uvicorn.error")


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):

    def __init__(self, repository: AndrewsArchitectRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        logger.info("[AndrewsArchitectUseCase] introduce_myself | request_data=%s", schema)
        return await self._repository.introduce_myself(schema)

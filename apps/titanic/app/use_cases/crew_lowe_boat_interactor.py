from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository

logger = logging.getLogger("uvicorn.error")


class LoweBoatInteractor(LoweBoatUseCase):

    def __init__(self, repository: LoweBoatRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        logger.info("[LoweBoatUseCase] introduce_myself | request_data=%s", schema)
        return await self._repository.introduce_myself(schema)

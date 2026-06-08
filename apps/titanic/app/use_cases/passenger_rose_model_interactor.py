from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

logger = logging.getLogger("uvicorn.error")


class RoseModelInteractor(RoseModelUseCase):

    def __init__(self, repository: RoseModelRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        logger.info("[RoseModelUseCase] introduce_myself | request_data=%s", schema)
        return await self._repository.introduce_myself(schema)

from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationResponse
from titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository

logger = logging.getLogger("uvicorn.error")


class RuthValidationInteractor(RuthValidationUseCase):

    def __init__(self, repository: RuthValidationRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        logger.info("[RuthValidationUseCase] introduce_myself | request_data=%s", schema)
        return await self._repository.introduce_myself(schema)

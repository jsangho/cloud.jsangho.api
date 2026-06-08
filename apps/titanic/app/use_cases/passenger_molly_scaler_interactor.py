from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository

logger = logging.getLogger("uvicorn.error")


class MollyScalerInteractor(MollyScalerUseCase):

    def __init__(self, repository: MollyScalerRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        logger.info("[MollyScalerUseCase] introduce_myself | request_data=%s", schema)
        return await self._repository.introduce_myself(schema)

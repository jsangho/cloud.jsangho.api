from __future__ import annotations

import logging

from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerQuery, MollyScalerResponse
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository

logger = logging.getLogger("uvicorn.error")


class MollyScalerInteractor(MollyScalerUseCase):

    def __init__(self, repository: MollyScalerRepository):
        self.repository = repository

    async def introduce_myself(self, query: MollyScalerQuery) -> MollyScalerResponse:
        logger.info("[MollyScalerUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        return await self.repository.introduce_myself(query)

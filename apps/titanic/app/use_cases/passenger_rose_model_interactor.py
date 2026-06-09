from __future__ import annotations

import logging

from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

logger = logging.getLogger("uvicorn.error")


class RoseModelInteractor(RoseModelUseCase):

    def __init__(self, repository: RoseModelRepository):
        self.repository = repository

    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        logger.info("[RoseModelUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        return await self.repository.introduce_myself(query)

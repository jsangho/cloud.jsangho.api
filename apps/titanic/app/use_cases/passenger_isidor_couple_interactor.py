from __future__ import annotations

import logging

from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleQuery, IsidorCoupleResponse
from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository

logger = logging.getLogger("uvicorn.error")


class IsidorCoupleInteractor(IsidorCoupleUseCase):

    def __init__(self, repository: IsidorCoupleRepository):
        self.repository = repository

    async def introduce_myself(self, query: IsidorCoupleQuery) -> IsidorCoupleResponse:
        logger.info("[IsidorCoupleUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        return await self.repository.introduce_myself(query)

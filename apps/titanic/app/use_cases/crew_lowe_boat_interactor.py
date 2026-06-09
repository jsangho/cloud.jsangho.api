from __future__ import annotations

import logging

from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository

logger = logging.getLogger("uvicorn.error")


class LoweBoatInteractor(LoweBoatUseCase):

    def __init__(self, repository: LoweBoatRepository):
        self.repository = repository

    async def introduce_myself(self, query: LoweBoatQuery) -> LoweBoatResponse:
        logger.info("[LoweBoatUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        return await self.repository.introduce_myself(query)

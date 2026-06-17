from __future__ import annotations

from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_port import LoweBoatPort

class LoweBoatInteractor(LoweBoatUseCase):

    def __init__(self, repository: LoweBoatPort):
        self.repository = repository

    async def introduce_myself(self, query: LoweBoatQuery) -> LoweBoatResponse:
        return await self.repository.introduce_myself(query)

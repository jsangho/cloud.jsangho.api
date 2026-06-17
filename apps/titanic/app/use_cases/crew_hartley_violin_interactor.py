from __future__ import annotations

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort

class HartleyViolinInteractor(HartleyViolinUseCase):

    def __init__(self, repository: HartleyViolinPort):
        self.repository = repository

    async def introduce_myself(self, query: HartleyViolinQuery) -> HartleyViolinResponse:
        return await self.repository.introduce_myself(query)

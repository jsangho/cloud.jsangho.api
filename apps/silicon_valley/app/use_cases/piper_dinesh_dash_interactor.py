from __future__ import annotations

from silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashQuery, DineshDashResponse
from silicon_valley.app.ports.input.piper_dinesh_dash_use_case import DineshDashUseCase
from silicon_valley.app.ports.output.piper_dinesh_dash_port import DineshDashPort


class DineshDashInteractor(DineshDashUseCase):

    def __init__(self, repository: DineshDashPort):
        self.repository = repository

    async def introduce_myself(self, query: DineshDashQuery) -> DineshDashResponse:
        return await self.repository.introduce_myself(query)

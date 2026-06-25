from __future__ import annotations

from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooQuery, DunnCooResponse
from silicon_valley.app.ports.input.piper_dunn_coo_use_case import DunnCooUseCase
from silicon_valley.app.ports.output.piper_dunn_coo_port import DunnCooPort


class DunnCooInteractor(DunnCooUseCase):
    def __init__(self, repository: DunnCooPort):
        self.repository = repository

    async def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        return await self.repository.introduce_myself(query)

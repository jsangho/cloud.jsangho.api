from __future__ import annotations

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository

class AndrewsArchitectInteractor(AndrewsArchitectUseCase):

    def __init__(self, repository: AndrewsArchitectRepository):
        self.repository = repository

    async def introduce_myself(self, query: AndrewsArchitectQuery) -> AndrewsArchitectResponse:
        return await self.repository.introduce_myself(query)

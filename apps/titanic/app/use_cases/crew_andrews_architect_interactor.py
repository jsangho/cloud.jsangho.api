from __future__ import annotations

from typing import Any

from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    """Andrews Blueprint 조회 유스케이스."""

    def __init__(self, repository: AndrewsArchitectRepository) -> None:
        self._repository = repository

    async def get_architect(self) -> dict[str, Any]:
        return await self._repository.get_architect()

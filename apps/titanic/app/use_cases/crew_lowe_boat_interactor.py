from __future__ import annotations

from typing import Any

from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository


class LoweBoatInteractor(LoweBoatUseCase):
    """Andrews Blueprint 조회 유스케이스."""

    def __init__(self, repository: LoweBoatRepository) -> None:
        self._repository = repository

    async def get_boat(self) -> dict[str, Any]:
        return await self._repository.get_boat()

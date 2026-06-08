from __future__ import annotations

from typing import Any

from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository


class RoseModelInteractor(RoseModelUseCase):
    """Rose 다이아몬드 조회 유스케이스."""

    def __init__(self, repository: RoseModelRepository) -> None:
        self._repository = repository

    async def get_model(self) -> dict[str, Any]:
        return await self._repository.get_model()

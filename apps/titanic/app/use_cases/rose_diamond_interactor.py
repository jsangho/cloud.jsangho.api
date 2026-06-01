from __future__ import annotations

from typing import Any

from titanic.app.ports.input.rose_diamond_use_case import RoseDiamondUseCase
from titanic.app.ports.output.rose_diamond_repository import RoseDiamondRepository


class RoseDiamondInteractor(RoseDiamondUseCase):
    """Rose 다이아몬드 조회 유스케이스."""

    def __init__(self, repository: RoseDiamondRepository) -> None:
        self._repository = repository

    async def get_diamond(self) -> dict[str, Any]:
        return await self._repository.get_diamond()

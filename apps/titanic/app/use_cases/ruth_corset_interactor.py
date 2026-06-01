from __future__ import annotations

from typing import Any

from titanic.app.ports.input.ruth_corset_use_case import RuthCorsetUseCase
from titanic.app.ports.output.ruth_corset_repository import RuthCorsetRepository


class RuthCorsetInteractor(RuthCorsetUseCase):
    """Ruth 코르셋 조회 유스케이스."""

    def __init__(self, repository: RuthCorsetRepository) -> None:
        self._repository = repository

    async def get_corset(self) -> dict[str, Any]:
        return await self._repository.get_corset()

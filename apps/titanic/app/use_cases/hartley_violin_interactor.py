from __future__ import annotations

from typing import Any

from titanic.app.ports.input.hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.hartley_violin_repository import HartleyViolinRepository


class HartleyViolinInteractor(HartleyViolinUseCase):
    """Hartley 바이올린 조회 유스케이스."""

    def __init__(self, repository: HartleyViolinRepository) -> None:
        self._repository = repository

    async def get_violin(self) -> dict[str, Any]:
        return await self._repository.get_violin()

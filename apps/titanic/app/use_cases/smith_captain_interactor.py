from __future__ import annotations

from typing import Any

from titanic.app.ports.input.smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.smith_captain_repository import SmithCaptainRepository


class SmithCaptainInteractor(SmithCaptainUseCase):
    """Smith 선장 조회 유스케이스."""

    def __init__(self, repository: SmithCaptainRepository) -> None:
        self._repository = repository

    async def get_captain(self) -> dict[str, Any]:
        return await self._repository.get_captain()

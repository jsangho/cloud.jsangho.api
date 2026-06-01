from __future__ import annotations

from typing import Any

from titanic.app.ports.input.cal_pistol_use_case import CalPistolUseCase
from titanic.app.ports.output.cal_pistol_repository import CalPistolRepository


class CalPistolInteractor(CalPistolUseCase):
    """Cal 권총 조회 유스케이스."""

    def __init__(self, repository: CalPistolRepository) -> None:
        self._repository = repository

    async def get_pistol(self) -> dict[str, Any]:
        return await self._repository.get_pistol()

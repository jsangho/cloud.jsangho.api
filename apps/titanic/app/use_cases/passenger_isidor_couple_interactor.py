from __future__ import annotations

from typing import Any

from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository


class IsidorCoupleInteractor(IsidorCoupleUseCase):
    """Isidor 침대 조회 유스케이스."""

    def __init__(self, repository: IsidorCoupleRepository) -> None:
        self._repository = repository

    async def get_couple(self) -> dict[str, Any]:
        return await self._repository.get_couple()

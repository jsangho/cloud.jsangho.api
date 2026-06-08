from __future__ import annotations

from typing import Any

from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository


class MollyScalerInteractor(MollyScalerUseCase):
    """Cal 권총 조회 유스케이스."""

    def __init__(self, repository: MollyScalerRepository) -> None:
        self._repository = repository

    async def get_scaler(self) -> dict[str, Any]:
        return await self._repository.get_scaler()

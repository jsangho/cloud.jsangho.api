from __future__ import annotations

from typing import Any

from titanic.app.ports.input.isidor_bed_use_case import IsidorBedUseCase
from titanic.app.ports.output.isidor_bed_repository import IsidorBedRepository


class IsidorBedInteractor(IsidorBedUseCase):
    """Isidor 침대 조회 유스케이스."""

    def __init__(self, repository: IsidorBedRepository) -> None:
        self._repository = repository

    async def get_bed(self) -> dict[str, Any]:
        return await self._repository.get_bed()

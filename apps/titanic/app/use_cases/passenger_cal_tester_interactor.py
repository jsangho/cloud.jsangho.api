from __future__ import annotations

from typing import Any

from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository


class CalTesterInteractor(CalTesterUseCase):
    """Cal 권총 조회 유스케이스."""

    def __init__(self, repository: CalTesterRepository) -> None:
        self._repository = repository

    async def get_tester(self) -> dict[str, Any]:
        return await self._repository.get_tester()

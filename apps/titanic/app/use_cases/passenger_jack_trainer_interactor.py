from __future__ import annotations

from typing import Any

from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository


class JackTrainerInteractor(JackTrainerUseCase):
    """Jack 스케치 조회 유스케이스."""

    def __init__(self, repository: JackTrainerRepository) -> None:
        self._repository = repository

    async def get_trainer(self) -> dict[str, Any]:
        return await self._repository.get_trainer()

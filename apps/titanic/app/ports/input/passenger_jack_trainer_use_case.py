from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackTrainerUseCase(ABC):
    """`/titanic/jack/*` inbound(jack_trainer_router) 입력 포트."""

    @abstractmethod
    async def get_trainer(self) -> dict[str, Any]:
        """스케치 조회 (`GET /sketch`)."""
        ...

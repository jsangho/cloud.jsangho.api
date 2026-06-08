from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LoweBoatUseCase(ABC):
    """`/titanic/andrews/*` inbound(lowe_boat_router) 입력 포트."""

    @abstractmethod
    async def get_boat(self) -> dict[str, Any]:
        """설계도 조회 (`GET /blueprint`)."""
        ...

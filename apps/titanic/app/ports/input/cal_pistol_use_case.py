from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CalPistolUseCase(ABC):
    """`/titanic/cal/*` inbound(cal_pistol_router) 입력 포트."""

    @abstractmethod
    async def get_pistol(self) -> dict[str, Any]:
        """권총 조회 (`GET /pistol`)."""
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SmithCaptainUseCase(ABC):
    """`/titanic/smith/*` inbound(smith_captain_router) 입력 포트."""

    @abstractmethod
    async def get_captain(self) -> dict[str, Any]:
        """선장 조회 (`GET /captain`)."""
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AndrewsArchitectUseCase(ABC):
    """`/titanic/andrews/*` inbound(andrews_architect_router) 입력 포트."""

    @abstractmethod
    async def get_architect(self) -> dict[str, Any]:
        """설계도 조회 (`GET /blueprint`)."""
        ...

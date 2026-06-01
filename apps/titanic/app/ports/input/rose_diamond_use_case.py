from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseDiamondUseCase(ABC):
    """`/titanic/rose/*` inbound(rose_diamond_router) 입력 포트."""

    @abstractmethod
    async def get_diamond(self) -> dict[str, Any]:
        """다이아몬드 조회 (`GET /diamond`)."""
        ...

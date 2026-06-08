from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class HartleyViolinUseCase(ABC):
    """`/titanic/hartley/*` inbound(hartley_violin_router) 입력 포트."""

    @abstractmethod
    async def get_violin(self) -> dict[str, Any]:
        """바이올린 조회 (`GET /violin`)."""
        ...

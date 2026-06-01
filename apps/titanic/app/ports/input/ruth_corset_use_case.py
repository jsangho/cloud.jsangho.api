from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RuthCorsetUseCase(ABC):
    """`/titanic/ruth/*` inbound(ruth_corset_router) 입력 포트."""

    @abstractmethod
    async def get_corset(self) -> dict[str, Any]:
        """코르셋 조회 (`GET /corset`)."""
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseModelUseCase(ABC):
    """`/titanic/rose/*` inbound(rose_model_router) 입력 포트."""

    @abstractmethod
    async def get_model(self) -> dict[str, Any]:
        """다이아몬드 조회 (`GET /diamond`)."""
        ...

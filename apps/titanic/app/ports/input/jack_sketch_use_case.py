from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackSketchUseCase(ABC):
    """`/titanic/jack/*` inbound(jack_sketch_router) 입력 포트."""

    @abstractmethod
    async def get_sketch(self) -> dict[str, Any]:
        """스케치 조회 (`GET /sketch`)."""
        ...

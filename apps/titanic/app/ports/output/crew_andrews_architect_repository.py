from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AndrewsArchitectRepository(ABC):
    """Andrews Blueprint 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_architect(self) -> dict[str, Any]:
        ...

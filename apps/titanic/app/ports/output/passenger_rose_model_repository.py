from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseModelRepository(ABC):
    """Rose 다이아몬드 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_model(self) -> dict[str, Any]:
        ...

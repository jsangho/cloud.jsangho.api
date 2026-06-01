from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class HartleyViolinRepository(ABC):
    """Hartley 바이올린 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_violin(self) -> dict[str, Any]:
        ...

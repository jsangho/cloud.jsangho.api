from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SmithCaptainRepository(ABC):
    """Smith 선장 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_captain(self) -> dict[str, Any]:
        ...

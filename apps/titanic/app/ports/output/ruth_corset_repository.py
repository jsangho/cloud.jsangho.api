from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RuthCorsetRepository(ABC):
    """Ruth 코르셋 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_corset(self) -> dict[str, Any]:
        ...

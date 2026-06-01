from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WalterRoasterRepository(ABC):
    """Walter Roaster 조회 데이터 출력 포트."""

    @abstractmethod
    async def list_page(
        self, *, page: int, page_size: int
    ) -> dict[str, Any]:
        ...

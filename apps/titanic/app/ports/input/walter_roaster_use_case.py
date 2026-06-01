from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WalterRoasterUseCase(ABC):
    """`/titanic/walter-roaster/*` inbound(walter_roaster_router) 입력 포트."""

    @abstractmethod
    async def list_page(
        self,
        *,
        page: int,
        page_size: int,
    ) -> dict[str, Any]:
        """탑승자 목록 조회 (`GET /openfile`)."""
        ...

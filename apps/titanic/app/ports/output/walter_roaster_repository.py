from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery


class WalterRoasterRepository(ABC):
    """월터의 승객 명단 관리 저장소."""

    @abstractmethod
    def introduce_myself(self, query: WalterRoasterQuery, *, trace: bool = True) -> None:
        """월터 자기소개 메소드."""
        ...

    @abstractmethod
    async def list_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        """Neon `titanic_persons` + `titanic_bookings` 페이징 조회."""
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery


class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterQuery:
        """월터 자기소개 메소드 (`GET /myself`)."""
        ...

    @abstractmethod
    async def openfile(
        self,
        query: WalterRoasterQuery,
        *,
        page: int,
        page_size: int,
    ) -> dict[str, Any]:
        """Neon `titanic_persons` + `titanic_bookings` 페이징 조회 (`GET /openfile`)."""
        ...


def get_walter_roaster_use_case() -> WalterRoasterUseCase:
    raise RuntimeError(
        "get_walter_roaster_use_case dependency is not configured. "
        "Wire Depends in walter_roaster_router."
    )

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse


class WalterRoasterRepository(ABC):

    @abstractmethod
    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        pass

    @abstractmethod
    async def list_openfile_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        ...

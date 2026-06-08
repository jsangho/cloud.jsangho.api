from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse


class WalterRoasterRepository(ABC):
    """승객 명단 관리 저장소."""

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터의 자기소개 메소드'''
        pass
    @abstractmethod
    async def list_openfile_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        """승객 명단 페이지 조회."""
        ...

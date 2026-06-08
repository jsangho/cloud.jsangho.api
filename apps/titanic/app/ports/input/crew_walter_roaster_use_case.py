from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse


class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        """윌터 자기소개 메소드 (`GET /myself`)."""
        ...

    @abstractmethod
    async def list_openfile_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        """승객 명단 페이지 조회 (`GET /openfile`)."""
        ...


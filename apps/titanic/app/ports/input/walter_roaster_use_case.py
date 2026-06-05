from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.walter_roaster_dto import WalterRoasterResponse


class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        """월터 자기소개 메소드 (`GET /myself`)."""
        ...


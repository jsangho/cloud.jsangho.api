from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse


class SmithCaptainUseCase(ABC):
    """`/titanic/smith/*` inbound(smith_captain_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        """스미스 선장 자기소개 메소드 (`GET /myself`)."""
        ...

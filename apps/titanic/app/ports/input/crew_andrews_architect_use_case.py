from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse


class AndrewsArchitectUseCase(ABC):
    """`/titanic/andrews/*` inbound(andrews_architect_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        """앤드류스 자기소개 메소드 (`GET /myself`)."""
        ...

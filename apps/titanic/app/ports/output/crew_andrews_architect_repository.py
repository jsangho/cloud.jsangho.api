from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse


class AndrewsArchitectRepository(ABC):
    """Andrews Architect 출력 포트."""

    @abstractmethod
    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        """앤드류스 자기소개 저장소 메소드."""
        ...

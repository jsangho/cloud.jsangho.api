from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema


class SmithCaptainRepository(ABC):

    @abstractmethod
    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        pass

    @abstractmethod
    async def chat(self, schema: ChatSchema) -> SmithCaptainResponse:
        pass


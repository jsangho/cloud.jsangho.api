from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema
from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainChatResponse,
    SmithCaptainQuery,
    SmithCaptainResponse,
)


class SmithCaptainUseCase(ABC):
    """`/titanic/smith/*` inbound(smith_captain_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        """스미스 선장 자기소개 메소드 (`GET /myself`)."""
        ...

    @abstractmethod
    async def chat(self, schema: ChatSchema) -> SmithCaptainChatResponse:
        """채팅창 자연어 입력에 대한 선장 응답"""
        ...

    @abstractmethod
    def chat_stream(self, schema: ChatSchema) -> Iterator[str]:
        """스트리밍 채팅 응답"""
        ...

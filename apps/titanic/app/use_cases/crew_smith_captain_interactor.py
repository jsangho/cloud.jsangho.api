from __future__ import annotations

import logging
from collections.abc import Iterator

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema
from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainChatCommand,
    SmithCaptainChatResponse,
    SmithCaptainChatTurnDto,
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = logging.getLogger("uvicorn.error")


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def chat(self, schema: ChatSchema) -> SmithCaptainChatResponse:
        command = self._to_command(schema)
        return await self.repository.chat(command)

    def chat_stream(self, schema: ChatSchema) -> Iterator[str]:
        command = self._to_command(schema)
        return self.repository.chat_stream(command)

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        logger.info(
            "[SmithCaptainUseCase] introduce_myself | request_data=%s",
            f"id={query.id} name={query.name!r}",
        )
        return await self.repository.introduce_myself(query)

    @staticmethod
    def _to_command(schema: ChatSchema) -> SmithCaptainChatCommand:
        messages = tuple(
            SmithCaptainChatTurnDto(role=message.role, text=message.text.strip())
            for message in schema.messages
            if message.text.strip()
        )
        return SmithCaptainChatCommand(messages=messages, stream=schema.stream)

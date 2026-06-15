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
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = logging.getLogger("uvicorn.error")


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def chat(self, schema: ChatSchema,
                jack: JackTrainerUseCase,
                rose: RoseModelUseCase,
                ) -> SmithCaptainChatResponse:
        # schema 에 들어있는 messages 내용 보기
        messages = schema.messages
        logger.info("[SmithCaptainInteractor] chat | messages=%s", messages)

        return SmithCaptainChatResponse(reply="1309명 입니다")

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        return await self.repository.introduce_myself(query)

    @staticmethod
    def _to_command(schema: ChatSchema) -> SmithCaptainChatCommand:
        messages = tuple(
            SmithCaptainChatTurnDto(role=message.role, text=message.text.strip())
            for message in schema.messages
            if message.text.strip()
        )
        return SmithCaptainChatCommand(messages=messages, stream=schema.stream)

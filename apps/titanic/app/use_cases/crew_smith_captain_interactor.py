from __future__ import annotations

import logging

from titanic.app.dtos.crew_smith_captain_dto import (
    ChatResponse,
    SmithCaptainChatCommand,
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = logging.getLogger(__name__)


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def chat(
        self,
        command: SmithCaptainChatCommand,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
    ) -> ChatResponse:
        logger.info("[SmithCaptainInteractor] chat 진입 | messages=%s", command.messages)
        return "1309명 입니다"

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(query)

 
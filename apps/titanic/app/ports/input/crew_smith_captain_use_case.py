from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_smith_captain_dto import (
    ChatResponse,
    SmithCaptainChatCommand,
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase


class SmithCaptainUseCase(ABC):
    """`/titanic/smith/*` inbound(smith_captain_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        """스미스 선장 자기소개 메소드 (`GET /myself`)."""
        ...

    @abstractmethod
    async def chat(
        self,
        command: SmithCaptainChatCommand,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
    ) -> ChatResponse:
        """채팅창 자연어 입력에 대한 선장 응답"""
        ...
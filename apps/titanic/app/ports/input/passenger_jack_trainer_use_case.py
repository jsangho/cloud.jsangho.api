from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse


class JackTrainerUseCase(ABC):
    """`/titanic/jack/*` inbound(jack_trainer_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        """잭 도슨 트레이너의 자기소개 메소드 (`GET /myself`)."""
        ...

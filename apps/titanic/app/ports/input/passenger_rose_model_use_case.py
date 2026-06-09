from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse


class RoseModelUseCase(ABC):
    """`/titanic/rose/*` inbound(rose_model_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        """로즈 드윗 부카터의 자기소개 메소드 (`GET /myself`)."""
        ...

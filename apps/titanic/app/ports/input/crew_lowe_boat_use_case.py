from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse


class LoweBoatUseCase(ABC):
    """`/titanic/lowe/*` inbound(lowe_boat_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, query: LoweBoatQuery) -> LoweBoatResponse:
        """로우 자기소개 메소드 (`GET /myself`)."""
        ...

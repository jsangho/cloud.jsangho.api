from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema
from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleResponse


class IsidorCoupleUseCase(ABC):
    """`/titanic/isidor/*` inbound(isidor_couple_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        """이시도르 & 이다 스트라우스 부부의 자기소개 메소드 (`GET /myself`)."""
        ...

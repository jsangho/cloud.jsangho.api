from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationResponse


class RuthValidationUseCase(ABC):
    """`/titanic/ruth/*` inbound(ruth_validation_router) 입력 포트."""

    @abstractmethod
    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        """루스 드윗 부카터의 자기소개 메소드 (`GET /myself`)."""
        ...

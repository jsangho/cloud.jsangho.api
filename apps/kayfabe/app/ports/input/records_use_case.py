from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.inbound.api.schemas.records_schema import (
    CompetitorListResponseSchema,
    CompetitorProfileResponseSchema,
)


class RecordsUseCase(ABC):
    """`/records/*` inbound(records_router)가 호출하는 입력 포트."""

    @abstractmethod
    async def list_competitors(self, *, q: str | None = None) -> CompetitorListResponseSchema:
        """Neon에 동기화된 PLE 카드 기준 출전 선수 목록."""
        ...

    @abstractmethod
    async def get_competitor_profile(self, name: str) -> CompetitorProfileResponseSchema:
        """선수별 PLE 승패 기록."""
        ...

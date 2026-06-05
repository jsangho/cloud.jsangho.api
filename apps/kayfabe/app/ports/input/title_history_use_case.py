from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.inbound.api.schemas.title_history_schema import (
    CompetitorTitleHistoryResponseSchema,
)


class TitleHistoryUseCase(ABC):
    @abstractmethod
    async def get_competitor_title_history(self, name: str) -> CompetitorTitleHistoryResponseSchema:
        ...

    @abstractmethod
    async def sync_from_real_catalog(self) -> int:
        """실제 WWE 타이틀 획득 카탈로그로 NeonDB 재생성."""
        ...

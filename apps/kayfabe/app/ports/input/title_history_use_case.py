from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.title_history_dto import CompetitorTitleHistoryDto


class TitleHistoryUseCase(ABC):
    """`/title-history/*` inbound(title_history_router) 입력 포트."""

    @abstractmethod
    async def get_competitor_title_history(self, name: str) -> CompetitorTitleHistoryDto:
        ...

    @abstractmethod
    async def sync_from_real_catalog(self) -> int:
        """실제 WWE 타이틀 획득 카탈로그로 NeonDB 재생성."""
        ...

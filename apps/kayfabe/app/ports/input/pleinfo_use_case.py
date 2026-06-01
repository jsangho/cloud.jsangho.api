from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.ports.input.ple_schema import (
    PleAiStatsSchema,
    PleBoardSchema,
    PleEventSummarySchema,
)


class PleInfoUseCase(ABC):
    """`/ple/*` GET inbound(pleinfo_router)가 호출하는 조회 입력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def list_events(self) -> list[PleEventSummarySchema]:
        """Neon에 동기화된 PLE 이벤트 목록."""
        ...

    @abstractmethod
    async def get_ai_stats(self) -> PleAiStatsSchema:
        """AI 예측 누적 적중률·최근 채점 기록."""
        ...

    @abstractmethod
    async def get_board(
        self,
        *,
        slug: str,
        client_id: str | None = None,
        user_id: int | None = None,
    ) -> PleBoardSchema:
        """PLE 경기 보드(카드·사이트 투표·내 예측)."""
        ...

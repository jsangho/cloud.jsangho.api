from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.ranking_dto import RankingsDto


class RankingUseCase(ABC):
    """`/rankings` inbound(ranking_router) 입력 포트."""

    @abstractmethod
    async def list_rankings(
        self,
        *,
        limit: int = 120,
        nickname: str | None = None,
    ) -> RankingsDto:
        """PLE 예측 순위 (점수·적중률)."""
        ...

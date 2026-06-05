from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.inbound.api.schemas.ranking_schema import RankingsResponseSchema


class RankingUseCase(ABC):
    """`/rankings` inbound(ranking_router)가 호출하는 입력 포트."""

    @abstractmethod
    async def list_rankings(
        self,
        *,
        limit: int = 120,
        nickname: str | None = None,
    ) -> RankingsResponseSchema:
        """PLE 예측 순위 (점수·적중률)."""
        ...

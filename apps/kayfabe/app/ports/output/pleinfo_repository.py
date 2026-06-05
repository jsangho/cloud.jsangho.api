from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.inbound.api.schemas.ple_schema import PleAiStatsSchema
from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel, PleMatchModel, PlePredictionModel


class PleInfoRepository(ABC):
    """PLE 조회 데이터를 제공하는 출력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def list_events(self) -> list[PleEventModel]:
        ...

    @abstractmethod
    async def get_event_by_slug(self, slug: str) -> PleEventModel | None:
        ...

    @abstractmethod
    async def get_prediction_by_user(
        self, match_id: int, user_id: int
    ) -> PlePredictionModel | None:
        ...

    @abstractmethod
    async def get_prediction(
        self, match_id: int, client_id: str
    ) -> PlePredictionModel | None:
        ...

    @staticmethod
    @abstractmethod
    def aggregate_votes(
        match: PleMatchModel,
    ) -> tuple[dict[str, int | list[int]], str | None]:
        ...

    @abstractmethod
    async def get_ai_stats(self) -> PleAiStatsSchema:
        ...

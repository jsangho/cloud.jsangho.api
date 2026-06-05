from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.inbound.api.schemas.ple_schema import MatchResultSchema, PleEventSyncSchema
from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel, PleMatchModel, PlePredictionModel


class PleRepository(ABC):
    """PLE 쓰기 데이터를 영속화하는 출력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def user_exists(self, *, user_id: int) -> bool:
        """예측 저장 전 로그인 회원 존재 여부 확인."""
        ...

    @abstractmethod
    async def flush(self) -> None:
        """현재 트랜잭션 변경 사항을 DB에 반영."""
        ...

    @abstractmethod
    async def get_event_by_slug(self, slug: str) -> PleEventModel | None:
        """slug로 PLE 이벤트(매치 포함) 조회 — 쓰기 전 검증용."""
        ...

    @abstractmethod
    async def upsert_event_from_sync(self, payload: PleEventSyncSchema) -> PleEventModel:
        """프론트 매치 카드를 Neon에 upsert (`sync_event`)."""
        ...

    @abstractmethod
    async def upsert_prediction(
        self, match_id: int, client_id: str, pick: str, user_id: int
    ) -> PlePredictionModel:
        """경기 예측 저장 (`record_prediction`, `record_predictions_batch`)."""
        ...

    @abstractmethod
    async def set_match_result(
        self,
        slug: str,
        match_key: str,
        result: MatchResultSchema,
        status: str | None = None,
    ) -> PleMatchModel | None:
        """경기 결과 저장 (`set_match_result`, `set_match_results_batch`, `sync_event`)."""
        ...

    @abstractmethod
    async def refresh_all_match_point_values(self) -> int:
        """랭킹 집계 전 전체 매치 점수 재계산."""
        ...

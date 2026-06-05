from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.inbound.api.schemas.ple_schema import (
    BatchPredictionRequestSchema,
    BatchResultsRequestSchema,
    MatchResultUpdateSchema,
    PleBoardSchema,
    PleEventSyncSchema,
    PredictionRequestSchema,
)


class PleUseCase(ABC):
    """`/ple/*` POST inbound(ple_router)가 호출하는 입력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def sync_event(self, *, payload: PleEventSyncSchema) -> PleBoardSchema:
        """프론트 매치 카드를 Neon에 upsert (`POST /{slug}/sync-from-client`)."""
        ...

    @abstractmethod
    async def record_predictions_batch(
        self, *, slug: str, body: BatchPredictionRequestSchema
    ) -> PleBoardSchema:
        """경기 예측 일괄 저장 (`POST /{slug}/predictions/batch`)."""
        ...

    @abstractmethod
    async def set_match_results_batch(
        self, *, slug: str, body: BatchResultsRequestSchema
    ) -> PleBoardSchema:
        """경기 결과 일괄 등록 (`POST /{slug}/results/batch`)."""
        ...

    @abstractmethod
    async def record_prediction(
        self, *, slug: str, match_key: str, body: PredictionRequestSchema
    ) -> PleBoardSchema:
        """경기 예측 1회 저장 (`POST /{slug}/matches/{match_key}/predict`)."""
        ...

    @abstractmethod
    async def set_match_result(
        self, *, slug: str, match_key: str, body: MatchResultUpdateSchema
    ) -> PleBoardSchema:
        """경기 결과 등록·갱신 (`POST /{slug}/matches/{match_key}/result`)."""
        ...

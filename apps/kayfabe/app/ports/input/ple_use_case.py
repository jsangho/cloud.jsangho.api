from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.ple_dto import (
    BatchPredictionCommand,
    BatchResultsCommand,
    MatchResultUpdateCommand,
    PleBoardDto,
    PleEventSyncCommand,
    PredictionCommand,
)


class PleUseCase(ABC):
    """`/ple/*` POST inbound(ple_router) 입력 포트."""

    @abstractmethod
    async def sync_event(self, *, payload: PleEventSyncCommand) -> PleBoardDto:
        """프론트 매치 카드를 Neon에 upsert (`POST /{slug}/sync-from-client`)."""
        ...

    @abstractmethod
    async def record_predictions_batch(
        self, *, slug: str, body: BatchPredictionCommand
    ) -> PleBoardDto:
        """경기 예측 일괄 저장 (`POST /{slug}/predictions/batch`)."""
        ...

    @abstractmethod
    async def set_match_results_batch(
        self, *, slug: str, body: BatchResultsCommand
    ) -> PleBoardDto:
        """경기 결과 일괄 등록 (`POST /{slug}/results/batch`)."""
        ...

    @abstractmethod
    async def record_prediction(
        self, *, slug: str, match_key: str, body: PredictionCommand
    ) -> PleBoardDto:
        """경기 예측 1회 저장 (`POST /{slug}/matches/{match_key}/predict`)."""
        ...

    @abstractmethod
    async def set_match_result(
        self, *, slug: str, match_key: str, body: MatchResultUpdateCommand
    ) -> PleBoardDto:
        """경기 결과 등록·갱신 (`POST /{slug}/matches/{match_key}/result`)."""
        ...

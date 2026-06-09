from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.ple_dto import (
    MatchResultDto,
    PleEventSnapshotDto,
    PleEventSyncCommand,
)


class PleRepository(ABC):
    """PLE 쓰기 출력 포트."""

    @abstractmethod
    async def user_exists(self, *, user_id: int) -> bool:
        """예측 저장 전 로그인 회원 존재 여부 확인."""
        ...

    @abstractmethod
    async def flush(self) -> None:
        """현재 트랜잭션 변경 사항을 DB에 반영."""
        ...

    @abstractmethod
    async def get_event_by_slug(self, slug: str) -> PleEventSnapshotDto | None:
        """slug로 PLE 이벤트 스냅샷 조회 — 쓰기 전 검증용."""
        ...

    @abstractmethod
    async def upsert_event_from_sync(self, payload: PleEventSyncCommand) -> PleEventSnapshotDto:
        """프론트 매치 카드를 Neon에 upsert."""
        ...

    @abstractmethod
    async def upsert_prediction(
        self, match_id: int, client_id: str, pick: str, user_id: int
    ) -> None:
        """경기 예측 저장."""
        ...

    @abstractmethod
    async def set_match_result(
        self,
        slug: str,
        match_key: str,
        result: MatchResultDto,
        status: str | None = None,
    ) -> bool:
        """경기 결과 저장. 성공 시 True."""
        ...

    @abstractmethod
    async def mark_event_finished(self, *, event_id: int, finished_at) -> None:
        """이벤트 상태를 finished로 갱신."""
        ...

    @abstractmethod
    async def refresh_all_match_point_values(self) -> int:
        """랭킹 집계 전 전체 매치 점수 재계산."""
        ...

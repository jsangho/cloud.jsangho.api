from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.ple_dto import PleAiStatsDto, PleEventReadDto


class PleInfoRepository(ABC):
    """PLE 조회 출력 포트."""

    @abstractmethod
    async def list_events(self) -> list[PleEventReadDto]:
        ...

    @abstractmethod
    async def get_event_by_slug(self, slug: str) -> PleEventReadDto | None:
        ...

    @abstractmethod
    async def get_prediction_pick_by_user(self, match_id: int, user_id: int) -> str | None:
        ...

    @abstractmethod
    async def get_prediction_pick(self, match_id: int, client_id: str) -> str | None:
        ...

    @abstractmethod
    async def aggregate_votes_for_match(
        self, *, match_id: int, fmt: str, card_json: str
    ) -> dict[str, int | list[int]]:
        """경기별 사이트 투표 집계."""
        ...

    @abstractmethod
    async def get_ai_stats(self) -> PleAiStatsDto:
        ...

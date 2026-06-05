from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel


class ResultRepository(ABC):
    """PLE 이벤트 결과 목록 조회 출력 포트."""

    @abstractmethod
    async def list_events_by_year(self, year: int) -> list[PleEventModel]:
        """연도별 PLE 이벤트 목록."""
        ...

from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel, PleMatchModel

class RecordsRepository(ABC):
    """PLE 카드(card_json)에서 출전 선수명을 수집하는 출력 포트."""

    @abstractmethod
    async def list_competitor_names(self) -> list[str]:
        """동기화된 전체 경기 카드에서 선수명 목록(중복 제거·정렬 전)."""
        ...

    @abstractmethod
    async def list_match_snapshots(self) -> list[tuple[PleEventModel, PleMatchModel]]:
        """Records 계산에 필요한 이벤트/경기 스냅샷(예측/투표 제외)."""
        ...

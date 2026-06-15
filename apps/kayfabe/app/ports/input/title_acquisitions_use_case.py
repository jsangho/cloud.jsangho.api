from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.championship_dto import ChampionshipBoardResponse
from kayfabe.app.dtos.title_history_dto import CompetitorTitleHistoryResponse


class TitleHistoryUseCase(ABC):
    """`/title-history/*` inbound(title_acquisitions_router) 입력 포트."""

    @abstractmethod
    async def get_competitor_title_history(self, name: str) -> CompetitorTitleHistoryResponse:
        ...

    @abstractmethod
    async def sync_from_real_catalog(self) -> int:
        """실제 WWE 타이틀 획득 카탈로그로 NeonDB 재생성."""
        ...


class ChampionshipUseCase(ABC):
    """`/championship` inbound(title_acquisitions_router > championship_router) 입력 포트."""

    @abstractmethod
    async def get_board(self) -> ChampionshipBoardResponse:
        """브랜드별 현역 챔피언 보드."""
        ...

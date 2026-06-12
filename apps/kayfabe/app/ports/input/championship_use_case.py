from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.championship_dto import ChampionshipBoardDto


class ChampionshipUseCase(ABC):
    """`/championship` inbound(championship_router) 입력 포트."""

    @abstractmethod
    async def get_board(self) -> ChampionshipBoardDto:
        """브랜드별 현역 챔피언 보드."""
        ...

from __future__ import annotations

from abc import ABC, abstractmethod

from kayfabe.app.dtos.championship_dto import ChampionshipBoardDto


class ChampionshipRepository(ABC):
    """현역 챔피언 데이터 소스 (카탈로그·DB 등)."""

    @abstractmethod
    async def get_board(self) -> ChampionshipBoardDto:
        ...

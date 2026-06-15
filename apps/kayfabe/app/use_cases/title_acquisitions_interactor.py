"""타이틀 획득 이력·현역 챔피언십 유스케이스."""

from __future__ import annotations

import logging

from kayfabe.app.dtos.championship_dto import ChampionshipBoardResponse
from kayfabe.app.dtos.myself_dto import MyselfQuery, MyselfRepository, MyselfResponse, MyselfUseCase
from kayfabe.app.dtos.title_history_dto import CompetitorTitleHistoryResponse, TitleAcquisitionResponse
from kayfabe.app.ports.input.title_acquisitions_use_case import ChampionshipUseCase, TitleHistoryUseCase
from kayfabe.app.ports.output.title_acquisitions_repository import (
    ChampionshipRepository,
    TitleHistoryRepository,
)
from kayfabe.app.services.records_scoring import normalize_name

logger = logging.getLogger("uvicorn.error")


class TitleHistoryInteractor(TitleHistoryUseCase):
    def __init__(self, *, title_history_repository: TitleHistoryRepository) -> None:
        self._title_history = title_history_repository

    async def sync_from_real_catalog(self) -> int:
        return await self._title_history.sync_from_real_catalog()

    async def _ensure_catalog_loaded(self) -> None:
        if await self._title_history.needs_real_resync():
            await self.sync_from_real_catalog()

    async def get_competitor_title_history(self, name: str) -> CompetitorTitleHistoryResponse:
        normalized = normalize_name(name)
        await self._ensure_catalog_loaded()
        rows = await self._title_history.list_by_competitor(competitor_name=normalized)
        return CompetitorTitleHistoryResponse(
            name=normalized,
            acquisitions=[
                TitleAcquisitionResponse(
                    belt_name=row.belt_name,
                    won_at=row.won_at,
                    won_at_slug=row.won_at_slug,
                    match_key=row.match_key,
                )
                for row in rows
            ],
        )


class ChampionshipInteractor(ChampionshipUseCase):
    def __init__(self, *, championship_repository: ChampionshipRepository) -> None:
        self._championship = championship_repository

    async def get_board(self) -> ChampionshipBoardResponse:
        logger.info("[ChampionshipInteractor] get_board -> Repository")
        board = await self._championship.get_board()
        logger.info(
            "[ChampionshipInteractor] get_board <- Repository brands=%d as_of=%s",
            len(board.brands),
            board.as_of,
        )
        return board


class TitleHistoryMyselfInteractor(MyselfUseCase):
    def __init__(self, repository: MyselfRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, query: MyselfQuery) -> MyselfResponse:
        return await self.repository.introduce_myself(query)


class ChampionshipMyselfInteractor(MyselfUseCase):
    def __init__(self, repository: MyselfRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, query: MyselfQuery) -> MyselfResponse:
        return await self.repository.introduce_myself(query)


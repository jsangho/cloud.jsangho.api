from __future__ import annotations

import logging

from kayfabe.app.dtos.championship_dto import ChampionshipBoardDto
from kayfabe.app.ports.input.championship import ChampionshipUseCase
from kayfabe.app.ports.output.championship_repository import ChampionshipRepository

logger = logging.getLogger("uvicorn.error")


class ChampionshipInteractor(ChampionshipUseCase):
    def __init__(self, *, championship_repository: ChampionshipRepository) -> None:
        self._championship = championship_repository

    async def get_board(self) -> ChampionshipBoardDto:
        logger.info("[ChampionshipInteractor] get_board -> Repository")
        board = await self._championship.get_board()
        logger.info(
            "[ChampionshipInteractor] get_board <- Repository brands=%d as_of=%s",
            len(board.brands),
            board.as_of,
        )
        return board

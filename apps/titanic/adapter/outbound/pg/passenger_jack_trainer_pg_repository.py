from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class JackTrainerPgRepository(JackTrainerRepository):
    """Neon(Postgres) Jack ?¤ì?ì¹?ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_trainer(self) -> dict[str, Any]:
        logger.info("[%s] get_trainer -> Neon", _SRC)
        return {}

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from titanic.app.ports.output.passenger_ruth_survivor_repository import RuthSurvivorRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class RuthSurvivorPgRepository(RuthSurvivorRepository):
    """Neon(Postgres) Ruth ì½ë¥´??ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_survivor(self) -> dict[str, Any]:
        logger.info("[%s] get_survivor -> Neon", _SRC)
        return {}

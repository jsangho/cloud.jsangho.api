from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class LoweBoatPgRepository(LoweBoatRepository):
    """Neon(Postgres) Andrews Blueprint ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_boat(self) -> dict[str, Any]:
        logger.info("[%s] get_boat -> Neon", _SRC)
        return {}

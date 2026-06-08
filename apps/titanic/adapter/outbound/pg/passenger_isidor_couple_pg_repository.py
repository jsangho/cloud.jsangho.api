from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class IsidorCouplePgRepository(IsidorCoupleRepository):
    """Neon(Postgres) Isidor ì¹¨ë? ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_couple(self) -> dict[str, Any]:
        logger.info("[%s] get_couple -> Neon", _SRC)
        return {}

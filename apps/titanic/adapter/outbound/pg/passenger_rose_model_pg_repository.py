from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class RoseModelPgRepository(RoseModelRepository):
    """Neon(Postgres) Rose ?¤ì´?ëª¬??ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_model(self) -> dict[str, Any]:
        logger.info("[%s] get_model -> Neon", _SRC)
        return {}

from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import LAYER_LOG
from titanic.app.ports.output.rose_diamond_repository import RoseDiamondRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class RoseDiamondPgRepository(RoseDiamondRepository):
    """Neon(Postgres) Rose ?¤ì´?ëª¬??ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_diamond(self) -> dict[str, Any]:
        logger.info("[%s] get_diamond -> Neon", _SRC)
        return {}

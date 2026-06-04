from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import LAYER_LOG
from titanic.app.ports.output.ruth_corset_repository import RuthCorsetRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class RuthCorsetPgRepository(RuthCorsetRepository):
    """Neon(Postgres) Ruth ì½ë¥´??ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_corset(self) -> dict[str, Any]:
        logger.info("[%s] get_corset -> Neon", _SRC)
        return {}

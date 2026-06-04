from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import LAYER_LOG
from titanic.app.ports.output.hartley_violin_repository import HartleyViolinRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class HartleyViolinPgRepository(HartleyViolinRepository):
    """Neon(Postgres) Hartley ë°ì´?¬ë¦° ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_violin(self) -> dict[str, Any]:
        logger.info("[%s] get_violin -> Neon", _SRC)
        return {}

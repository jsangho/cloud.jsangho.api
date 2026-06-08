from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class SmithCaptainPgRepository(SmithCaptainRepository):
    """Neon(Postgres) Smith ? ì¥ ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_captain(self) -> dict[str, Any]:
        logger.info("[%s] get_captain -> Neon", _SRC)
        return {}

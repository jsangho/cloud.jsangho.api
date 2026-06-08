from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class CalTesterPgRepository(CalTesterRepository):
    """Neon(Postgres) Cal ê¶ì´ ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_tester(self) -> dict[str, Any]:
        logger.info("[%s] get_tester -> Neon", _SRC)
        return {}

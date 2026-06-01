from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.ports.output.cal_pistol_repository import CalPistolRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class CalPistolPgRepository(CalPistolRepository):
    """Neon(Postgres) Cal 권총 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_pistol(self) -> dict[str, Any]:
        logger.info("[%s] get_pistol -> Neon", _SRC)
        return {}

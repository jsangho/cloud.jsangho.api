from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.ports.output.smith_captain_repository import SmithCaptainRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class SmithCaptainPgRepository(SmithCaptainRepository):
    """Neon(Postgres) Smith 선장 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_captain(self) -> dict[str, Any]:
        logger.info("[%s] get_captain -> Neon", _SRC)
        return {}

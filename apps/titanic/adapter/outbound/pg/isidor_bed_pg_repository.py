from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.ports.output.isidor_bed_repository import IsidorBedRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class IsidorBedPgRepository(IsidorBedRepository):
    """Neon(Postgres) Isidor 침대 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_bed(self) -> dict[str, Any]:
        logger.info("[%s] get_bed -> Neon", _SRC)
        return {}

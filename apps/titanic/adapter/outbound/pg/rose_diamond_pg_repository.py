from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.ports.output.rose_diamond_repository import RoseDiamondRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class RoseDiamondPgRepository(RoseDiamondRepository):
    """Neon(Postgres) Rose 다이아몬드 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_diamond(self) -> dict[str, Any]:
        logger.info("[%s] get_diamond -> Neon", _SRC)
        return {}

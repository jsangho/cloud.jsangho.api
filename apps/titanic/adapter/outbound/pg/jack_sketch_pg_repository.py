from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.ports.output.jack_sketch_repository import JackSketchRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class JackSketchPgRepository(JackSketchRepository):
    """Neon(Postgres) Jack 스케치 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_sketch(self) -> dict[str, Any]:
        logger.info("[%s] get_sketch -> Neon", _SRC)
        return {}

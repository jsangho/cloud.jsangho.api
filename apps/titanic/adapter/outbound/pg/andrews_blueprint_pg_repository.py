from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import LAYER_LOG
from titanic.app.ports.output.andrews_blueprint_repository import AndrewsBlueprintRepository

logger = LAYER_LOG
_SRC = Path(__file__).name


class AndrewsBlueprintPgRepository(AndrewsBlueprintRepository):
    """Neon(Postgres) Andrews Blueprint ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_blueprint(self) -> dict[str, Any]:
        logger.info("[%s] get_blueprint -> Neon", _SRC)
        return {}

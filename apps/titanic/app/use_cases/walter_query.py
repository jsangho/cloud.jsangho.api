from __future__ import annotations

from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.ports.output.walter_repository import (
    WalterRepositoryImpl,
    WalterRepositoryPort,
)

logger = LAYER_LOG


class WalterQueryPort(Protocol):
    async def list_page(self, *, page: int, page_size: int) -> dict[str, Any]: ...


class WalterQueryImpl:
    def __init__(self, db: AsyncSession) -> None:
        self._repo: WalterRepositoryPort = WalterRepositoryImpl(db)

    async def list_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        logger.info("[WalterOpenFile] query -> repository page=%s page_size=%s", page, page_size)
        return await self._repo.list_page(page=page, page_size=page_size)

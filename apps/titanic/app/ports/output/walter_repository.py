from __future__ import annotations

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository

logger = LAYER_LOG


class WalterRepositoryPort(Protocol):
    """Walter 조회 출력 포트 (DB 접근)."""

    async def list_page(self, *, page: int, page_size: int) -> dict: ...


class WalterRepositoryImpl:
    def __init__(self, db: AsyncSession) -> None:
        self._pg = WalterPgRepository(db)

    async def list_page(self, *, page: int, page_size: int) -> dict:
        logger.info(
            "[WalterOpenFile] output_port(repository) -> pg_adapter page=%s page_size=%s",
            page,
            page_size,
        )
        return await self._pg.list_page(page=page, page_size=page_size)

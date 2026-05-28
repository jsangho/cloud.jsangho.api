from __future__ import annotations

from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.use_cases.walter_query import WalterQueryImpl, WalterQueryPort


logger = LAYER_LOG


class WalterUseCasePort(Protocol):
    """Walter inbound 조회 입력 포트."""

    async def list_page(self, *, page: int, page_size: int) -> dict[str, Any]: ...


class WalterUseCaseImpl:
    def __init__(self, db: AsyncSession) -> None:
        self._query: WalterQueryPort = WalterQueryImpl(db)

    async def list_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        logger.info(
            "[WalterOpenFile] use_case -> walter_query page=%s page_size=%s",
            page,
            page_size,
        )
        return await self._query.list_page(page=page, page_size=page_size)

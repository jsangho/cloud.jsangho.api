from __future__ import annotations

import logging
from typing import Any

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger("uvicorn.error")


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterRepository | None = None) -> None:
        self._repository = repository

    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        logger.info("[WalterRoasterUseCase] introduce_myself | request_data=%s", f"id={query.id} name={query.name!r}")
        if self._repository is None:
            return WalterRoasterResponse(id=query.id, name=query.name)
        return await self._repository.introduce_myself(query)

    async def list_openfile_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        logger.info(
            "[WalterRoasterUseCase] list_openfile_page | page=%s page_size=%s",
            page,
            page_size,
        )
        if self._repository is None:
            return {"page": page, "pageSize": page_size, "total": 0, "items": []}
        return await self._repository.list_openfile_page(page=page, page_size=page_size)

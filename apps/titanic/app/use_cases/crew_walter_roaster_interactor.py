from typing import Any

from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository
import logging

logger = logging.getLogger("uvicorn.error")


class WalterQuery:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        total, items = await self.repository.list_paginated(page, page_size)
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterRepository | None = None) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        logger.info("[WalterRoasterUseCase] introduce_myself | request_data=%s", schema)
        if self._repository is None:
            return WalterRoasterResponse(id=schema.id, name=schema.name)
        return await self._repository.introduce_myself(schema)

    async def list_openfile_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        logger.info(
            "[WalterRoasterUseCase] list_openfile_page | page=%s page_size=%s",
            page,
            page_size,
        )
        if self._repository is None:
            return {"page": page, "pageSize": page_size, "total": 0, "items": []}
        return await self._repository.list_openfile_page(page=page, page_size=page_size)

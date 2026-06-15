from __future__ import annotations

from typing import Any

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository

class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterRepository | None = None) -> None:
        self._repository = repository

    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        if self._repository is None:
            return WalterRoasterResponse(id=query.id, name=query.name)
        return await self._repository.introduce_myself(query)

    async def list_openfile_page(self, *, page: int, page_size: int) -> dict[str, Any]:
        if self._repository is None:
            return {"page": page, "pageSize": page_size, "total": 0, "items": []}
        return await self._repository.list_openfile_page(page=page, page_size=page_size)

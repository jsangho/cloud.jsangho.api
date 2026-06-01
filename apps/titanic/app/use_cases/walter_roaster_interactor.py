from __future__ import annotations

from pathlib import Path
from typing import Any

from core.database import walter_roaster_open_info
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository

_SRC = Path(__file__).name


class WalterRoasterInteractor(WalterRoasterUseCase):
    """Walter Roaster 목록 조회 유스케이스."""

    def __init__(self, repository: WalterRoasterRepository) -> None:
        self._repository = repository

    async def list_page(
        self,
        *,
        page: int,
        page_size: int,
    ) -> dict[str, Any]:
        walter_roaster_open_info(
            _SRC, "page=%s pageSize=%s -> use_case", page, page_size
        )
        return await self._repository.list_page(page=page, page_size=page_size)

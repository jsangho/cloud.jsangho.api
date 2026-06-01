from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db, walter_roaster_open_info
from titanic.adapter.inbound.api.schemas.walter_roaster_schema import (
    WalterRoasterPageResponse,
)
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase

_SRC = Path(__file__).name

walter_roaster_router = APIRouter(
    prefix="/titanic/walter-roaster", tags=["walter-roaster"]
)


def get_walter_roaster_use_case(
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterUseCase:
    from titanic.adapter.outbound.pg.walter_roaster_pg_repository import (
        WalterRoasterPgRepository,
    )
    from titanic.app.use_cases.walter_roaster_interactor import WalterRoasterInteractor

    return WalterRoasterInteractor(WalterRoasterPgRepository(db))


@walter_roaster_router.get(
    "/openfile",
    response_model=WalterRoasterPageResponse,
    response_model_by_alias=True,
)
async def openfile(
    page: int = 1,
    pageSize: int = 50,
    use_case: WalterRoasterUseCase = Depends(get_walter_roaster_use_case),
):
    """Neon DB(`titanic_passengers`)에서 데이터를 읽습니다."""
    walter_roaster_open_info(
        _SRC, "page=%s pageSize=%s -> inbound", page, pageSize
    )
    return await use_case.list_page(page=page, page_size=pageSize)

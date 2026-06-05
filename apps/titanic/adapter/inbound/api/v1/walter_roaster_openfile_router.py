from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from titanic.adapter.inbound.api.schemas.walter_roaster_schema import (
    WalterRoasterOpenfileResponse,
    WalterRoasterPassengerItem,
)
from titanic.adapter.outbound.pg.walter_roaster_pg_repository import WalterRoasterPgRepository

walter_roaster_openfile_router = APIRouter(
    prefix="/walter-roaster",
    tags=["walter-roaster"],
)

_DEFAULT_WALTER = {
    "id": 2,
    "name": "Walter Nichols",
    "memo": "타이타닉의 일등 항해사, 승객 명단 관리 담당",
}


@walter_roaster_openfile_router.get(
    "/openfile",
    response_model=WalterRoasterOpenfileResponse,
)
async def openfile(
    page: int = 1,
    pageSize: int = 50,
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterOpenfileResponse:
    page_result = await WalterRoasterPgRepository(session=db).list_openfile_page(
        page=page,
        page_size=pageSize,
    )
    return WalterRoasterOpenfileResponse(
        id=_DEFAULT_WALTER["id"],
        name=_DEFAULT_WALTER["name"],
        memo=_DEFAULT_WALTER["memo"],
        page=page_result["page"],
        pageSize=page_result["pageSize"],
        total=page_result["total"],
        items=[
            WalterRoasterPassengerItem.model_validate(item)
            for item in page_result["items"]
        ],
    )

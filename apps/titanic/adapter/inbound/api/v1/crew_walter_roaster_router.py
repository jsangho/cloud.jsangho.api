import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import (
    WalterRoasterOpenfileResponse,
    WalterRoasterPassengerItem,
    WalterRoasterSchema,
)
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import WalterRoasterPgRepository
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_walter_roaster_use_case

'''
영화 <타이타닉>에서 승객 명단을 관리하는
일등 항해사 윌터 와일딩(Walter Nichols / 혹은 윌리엄 머독 등 영화 속 관리자 캐릭터)
또는 승객 명단(Passenger List)을 다루는 '월터'라는 인물의 상황에 맞추어,
직관적이면서도 센스 있는 중간 키워드를 추천해 드립니다.
'''
logger = logging.getLogger(__name__)

walter_roaster_router = APIRouter(prefix="/walter", tags=["walter"])

_DEFAULT_WALTER = {
    "id": 2,
    "name": "Walter Nichols",
    "memo": "타이타닉의 일등 항해사, 승객 명단 관리 담당",
}


@walter_roaster_router.get("/myself")
async def introduce_myself(
    walter: WalterRoasterUseCase = Depends(get_walter_roaster_use_case),
) -> WalterRoasterResponse:
    return await walter.introduce_myself(
        WalterRoasterSchema(
            id=2,
            name="Walter Nichols",
            memo="타이타닉의 일등 항해사, 승객 명단 관리 담당",
        )
    )


@walter_roaster_router.get("/openfile", response_model=WalterRoasterOpenfileResponse)
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

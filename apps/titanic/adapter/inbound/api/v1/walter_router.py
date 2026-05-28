from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.app.ports.input.walter_use_case import WalterUseCaseImpl, WalterUseCasePort

router = APIRouter(prefix="/titanic/walter", tags=["walter"])


def get_walter_use_case(db: AsyncSession = Depends(get_db)) -> WalterUseCasePort:
    return WalterUseCaseImpl(db)


@router.get("/openfile")
async def openfile(
    page: int = 1,
    pageSize: int = 50,
    use_case: WalterUseCasePort = Depends(get_walter_use_case),
):
    """Neon DB(`titanic_passengers`)에서 데이터를 읽습니다.

    응답에서는 `sex` 컬럼을 `gender`로 변환해 반환합니다.
    """
    return await use_case.list_page(page=page, page_size=pageSize)

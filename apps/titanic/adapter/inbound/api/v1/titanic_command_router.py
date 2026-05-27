from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.inbound.schemas.titanic_request import TitanicPassengersUpsertRequest

router = APIRouter(prefix="/titanic/v1", tags=["titanic"])


@router.post("/passengers/upsert")
async def upsert_passengers(
    body: TitanicPassengersUpsertRequest,
    db: AsyncSession = Depends(get_db),
):
    # Hexagonal 연결은 이후 use-case/port 구현에서 처리합니다.
    # 지금은 스키마 연결용 스텁만 둡니다.
    return {"received": len(body.rows)}


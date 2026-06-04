from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from titanic.app.ports.input.rose_diamond_use_case import RoseDiamondUseCase

rose_diamond_router = APIRouter(prefix="/rose", tags=["rose"])


def get_rose_diamond_use_case(db: AsyncSession = Depends(get_db)) -> RoseDiamondUseCase:
    from titanic.adapter.outbound.pg.rose_diamond_pg_repository import RoseDiamondPgRepository
    from titanic.app.use_cases.rose_diamond_interactor import RoseDiamondInteractor

    return RoseDiamondInteractor(RoseDiamondPgRepository(db))


@rose_diamond_router.get("/diamond")
async def get_rose_diamond(
    use_case: RoseDiamondUseCase = Depends(get_rose_diamond_use_case),
):
    return await use_case.get_diamond()

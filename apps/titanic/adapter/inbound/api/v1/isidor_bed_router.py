from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.app.ports.input.isidor_bed_use_case import IsidorBedUseCase

isidor_bed_router = APIRouter(prefix="/titanic/isidor", tags=["isidor"])


def get_isidor_bed_use_case(db: AsyncSession = Depends(get_db)) -> IsidorBedUseCase:
    from titanic.adapter.outbound.pg.isidor_bed_pg_repository import IsidorBedPgRepository
    from titanic.app.use_cases.isidor_bed_interactor import IsidorBedInteractor

    return IsidorBedInteractor(IsidorBedPgRepository(db))


@isidor_bed_router.get("/bed")
async def get_isidor_bed(
    use_case: IsidorBedUseCase = Depends(get_isidor_bed_use_case),
):
    return await use_case.get_bed()

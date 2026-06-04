from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from titanic.app.ports.input.smith_captain_use_case import SmithCaptainUseCase

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


def get_smith_captain_use_case(
    db: AsyncSession = Depends(get_db),
) -> SmithCaptainUseCase:
    from titanic.adapter.outbound.pg.smith_captain_pg_repository import (
        SmithCaptainPgRepository,
    )
    from titanic.app.use_cases.smith_captain_interactor import SmithCaptainInteractor

    return SmithCaptainInteractor(SmithCaptainPgRepository(db))


@smith_captain_router.get("/captain")
async def get_smith_captain(
    use_case: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
):
    return await use_case.get_captain()

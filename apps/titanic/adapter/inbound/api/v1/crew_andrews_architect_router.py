from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase

andrews_architect_router = APIRouter(prefix="/andrews", tags=["andrews"])


def get_andrews_architect_use_case(
    db: AsyncSession = Depends(get_db),
) -> AndrewsArchitectUseCase:
    from titanic.adapter.outbound.pg.crew_andrews_architect_pg_repository import (
        AndrewsArchitectPgRepository,
    )
    from titanic.app.use_cases.crew_andrews_architect_interactor import AndrewsArchitectInteractor

    return AndrewsArchitectInteractor(AndrewsArchitectPgRepository(db))


@andrews_architect_router.get("/blueprint")
async def get_andrews_architect(
    use_case: AndrewsArchitectUseCase = Depends(get_andrews_architect_use_case),
):
    return await use_case.get_architect()

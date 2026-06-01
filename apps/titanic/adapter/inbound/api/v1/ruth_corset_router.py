from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.app.ports.input.ruth_corset_use_case import RuthCorsetUseCase

ruth_corset_router = APIRouter(prefix="/titanic/ruth", tags=["ruth"])


def get_ruth_corset_use_case(db: AsyncSession = Depends(get_db)) -> RuthCorsetUseCase:
    from titanic.adapter.outbound.pg.ruth_corset_pg_repository import RuthCorsetPgRepository
    from titanic.app.use_cases.ruth_corset_interactor import RuthCorsetInteractor

    return RuthCorsetInteractor(RuthCorsetPgRepository(db))


@ruth_corset_router.get("/corset")
async def get_ruth_corset(
    use_case: RuthCorsetUseCase = Depends(get_ruth_corset_use_case),
):
    return await use_case.get_corset()

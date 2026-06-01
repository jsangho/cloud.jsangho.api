from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.app.ports.input.hartley_violin_use_case import HartleyViolinUseCase

hartley_violin_router = APIRouter(prefix="/titanic/hartley", tags=["hartley"])


def get_hartley_violin_use_case(
    db: AsyncSession = Depends(get_db),
) -> HartleyViolinUseCase:
    from titanic.adapter.outbound.pg.hartley_violin_pg_repository import (
        HartleyViolinPgRepository,
    )
    from titanic.app.use_cases.hartley_violin_interactor import HartleyViolinInteractor

    return HartleyViolinInteractor(HartleyViolinPgRepository(db))


@hartley_violin_router.get("/violin")
async def get_hartley_violin(
    use_case: HartleyViolinUseCase = Depends(get_hartley_violin_use_case),
):
    return await use_case.get_violin()

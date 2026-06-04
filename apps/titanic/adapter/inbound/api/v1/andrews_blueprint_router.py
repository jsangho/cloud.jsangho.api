from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from titanic.app.ports.input.andrews_blueprint_use_case import AndrewsBlueprintUseCase

andrews_blueprint_router = APIRouter(prefix="/andrews", tags=["andrews"])


def get_andrews_blueprint_use_case(
    db: AsyncSession = Depends(get_db),
) -> AndrewsBlueprintUseCase:
    from titanic.adapter.outbound.pg.andrews_blueprint_pg_repository import (
        AndrewsBlueprintPgRepository,
    )
    from titanic.app.use_cases.andrews_blueprint_interactor import AndrewsBlueprintInteractor

    return AndrewsBlueprintInteractor(AndrewsBlueprintPgRepository(db))


@andrews_blueprint_router.get("/blueprint")
async def get_andrews_blueprint(
    use_case: AndrewsBlueprintUseCase = Depends(get_andrews_blueprint_use_case),
):
    return await use_case.get_blueprint()

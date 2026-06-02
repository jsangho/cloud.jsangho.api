from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.app.ports.input.jack_sketch_use_case import JackSketchUseCase

jack_sketch_router = APIRouter(prefix="/jack", tags=["jack"])


def get_jack_sketch_use_case(db: AsyncSession = Depends(get_db)) -> JackSketchUseCase:
    from titanic.adapter.outbound.pg.jack_sketch_pg_repository import JackSketchPgRepository
    from titanic.app.use_cases.jack_sketch_interactor import JackSketchInteractor

    return JackSketchInteractor(JackSketchPgRepository(db))


@jack_sketch_router.get("/sketch")
async def get_jack_sketch(
    use_case: JackSketchUseCase = Depends(get_jack_sketch_use_case),
):
    return await use_case.get_sketch()

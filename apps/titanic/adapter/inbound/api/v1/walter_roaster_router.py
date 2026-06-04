# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db, walter_roaster_open_info
from titanic.adapter.inbound.api.schemas.walter_roaster_schema import (
    WalterRoasterOpenFileResponse,
    WalterRoasterSchema,
)
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase

logger = logging.getLogger("uvicorn.error")
_SRC = Path(__file__).name
walter_roaster_router = APIRouter(prefix="/walter-roaster", tags=["walter-roaster"])


def get_walter_roaster_use_case(
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterUseCase:
    from titanic.adapter.outbound.pg.walter_roaster_pg_repository import (
        WalterRoasterPgRepository,
    )
    from titanic.app.use_cases.walter_roaster_interactor import WalterRoasterInteractor

    return WalterRoasterInteractor(WalterRoasterPgRepository(db))


def _to_query(schema: WalterRoasterSchema) -> WalterRoasterQuery:
    return WalterRoasterQuery(
        id=schema.id,
        name=schema.name,
        memo=schema.memo,
    )


def _to_schema(query: WalterRoasterQuery) -> WalterRoasterSchema:
    return WalterRoasterSchema(
        id=query.id,
        name=query.name,
        memo=query.memo,
    )


def _log_walter_router(schema: WalterRoasterSchema) -> None:
    logger.info("########################################################################################")
    logger.info("🆗[월터 라우터] 월터의 자기소개 글을 가져오는 API 호출")
    logger.info("💌ID: %s", schema.id)
    logger.info("👁‍🗨이름: %s", schema.name)
    logger.info("📝비고: %s", schema.memo)
    logger.info("########################################################################################")


@walter_roaster_router.get("/myself", response_model=WalterRoasterSchema)
async def introduce_myself(
    use_case: WalterRoasterUseCase = Depends(get_walter_roaster_use_case),
):
    schema = WalterRoasterSchema()
    _log_walter_router(schema)
    query = await use_case.introduce_myself(_to_query(schema))
    return _to_schema(query)


@walter_roaster_router.get("/openfile", response_model=WalterRoasterOpenFileResponse)
async def openfile(
    page: int = 1,
    pageSize: int = 50,
    use_case: WalterRoasterUseCase = Depends(get_walter_roaster_use_case),
):
    schema = WalterRoasterSchema()
    _log_walter_router(schema)
    walter_roaster_open_info(
        _SRC,
        "page=%s pageSize=%s -> inbound",
        page,
        pageSize,
    )
    return await use_case.openfile(_to_query(schema), page=page, page_size=pageSize)

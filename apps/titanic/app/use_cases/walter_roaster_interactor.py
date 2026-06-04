# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from core.matrix.oracle_database import walter_roaster_open_info
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger("uvicorn.error")
_SRC = Path(__file__).name


class WalterQuery:
    def __init__(self, repository: WalterRoasterRepository) -> None:
        self.repository = repository

    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        return await self.repository.list_page(page=page, page_size=page_size)


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterRepository) -> None:
        self._repository = repository
        self._walter_query = WalterQuery(repository)

    @staticmethod
    def _log_use_case(query: WalterRoasterQuery) -> None:
        logger.info("########################################################################################")
        logger.info("🆗[월터 유스케이스] 라우터에서 가져온 월터 정보")
        logger.info("💌ID: %s", query.id)
        logger.info("👁‍🗨이름: %s", query.name)
        logger.info("📝비고: %s", query.memo)
        logger.info("########################################################################################")

    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterQuery:
        self._log_use_case(query)
        self._repository.introduce_myself(query)
        return query

    async def openfile(
        self,
        query: WalterRoasterQuery,
        *,
        page: int,
        page_size: int,
    ) -> dict[str, Any]:
        self._log_use_case(query)
        walter_roaster_open_info(
            _SRC,
            "page=%s pageSize=%s -> use_case",
            page,
            page_size,
        )
        self._repository.introduce_myself(query, trace=False)
        page_result = await self._walter_query.list_paginated(page, page_size)
        return {
            "id": query.id,
            "name": query.name,
            "memo": query.memo,
            **page_result,
        }

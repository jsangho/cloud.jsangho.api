from __future__ import annotations

import logging

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = logging.getLogger("uvicorn.error")


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository: SmithCaptainRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        logger.info("[SmithCaptainUseCase] introduce_myself | request_data=%s", schema)
        return await self._repository.introduce_myself(schema)

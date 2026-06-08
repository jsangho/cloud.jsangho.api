from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = logging.getLogger("uvicorn.error")

class SmithCaptainPgRepository(SmithCaptainRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        logger.info("[SmithCaptainPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return SmithCaptainResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
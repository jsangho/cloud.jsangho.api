from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository

logger = logging.getLogger("uvicorn.error")

class AndrewsArchitectPgRepository(AndrewsArchitectRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        logger.info("[AndrewsArchitectPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return AndrewsArchitectResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository

logger = logging.getLogger("uvicorn.error")

class LoweBoatPgRepository(LoweBoatRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        logger.info("[LoweBoatPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return LoweBoatResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
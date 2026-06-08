from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema
from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleResponse
from titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository

logger = logging.getLogger("uvicorn.error")

class IsidorCouplePgRepository(IsidorCoupleRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        logger.info("[IsidorCouplePgRepository] introduce_myself 진입 | request_data=%s", schema)
        return IsidorCoupleResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )

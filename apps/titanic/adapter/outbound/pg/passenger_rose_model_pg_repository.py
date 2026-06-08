from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

logger = logging.getLogger("uvicorn.error")

class RoseModelPgRepository(RoseModelRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        logger.info("[RoseModelPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return RoseModelResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
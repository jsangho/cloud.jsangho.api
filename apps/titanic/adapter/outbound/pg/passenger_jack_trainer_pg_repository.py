from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger("uvicorn.error")

class JackTrainerPgRepository(JackTrainerRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        logger.info("[JackTrainerPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return JackTrainerResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
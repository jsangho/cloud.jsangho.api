from __future__ import annotations
import logging



from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger("uvicorn.error")


class JackTrainerPgRepository(JackTrainerRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        logger.info("[JackTrainerPgRepository] introduce_myself 진입 | request_data=%s", f"id={query.id} name={query.name!r}")
        return JackTrainerResponse(
            id=query.id * 10000,
            name= query.name + "이 레포지토리에 다녀옴",
        )

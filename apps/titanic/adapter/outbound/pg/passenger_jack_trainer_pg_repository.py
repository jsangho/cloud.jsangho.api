from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

class JackTrainerPgRepository(JackTrainerRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        return JackTrainerResponse(
            id=query.id * 10000,
            name= query.name + "이 레포지토리에 다녀옴",
        )

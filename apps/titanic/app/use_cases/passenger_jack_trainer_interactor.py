from __future__ import annotations

from kiwipiepy import Kiwi

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository
        self.kiwi = Kiwi()

    async def analayze_message_intent(self, user_message: str) -> dict:
        self.kiwi.global_config.space_tolerance = 2
        cleaned_text = self.kiwi.space(user_message, reset_whitespace=True)
        tokens = self.kiwi.tokenize(cleaned_text)
        keywords = [t.form for t in tokens if t.tag.startswith("NN")]
        
        return {"cleaned_text": cleaned_text, "keywords": keywords}

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        return await self.repository.introduce_myself(query)

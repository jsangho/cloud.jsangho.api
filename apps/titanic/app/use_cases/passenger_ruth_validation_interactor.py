from __future__ import annotations

from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse
from titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository

class RuthValidationInteractor(RuthValidationUseCase):

    def __init__(self, repository: RuthValidationRepository):
        self.repository = repository

    async def introduce_myself(self, query: RuthValidationQuery) -> RuthValidationResponse:
        return await self.repository.introduce_myself(query)

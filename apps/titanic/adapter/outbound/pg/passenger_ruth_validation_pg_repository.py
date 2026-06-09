from __future__ import annotations
import logging



from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse
from titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository

logger = logging.getLogger("uvicorn.error")


class RuthValidationPgRepository(RuthValidationRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RuthValidationQuery) -> RuthValidationResponse:
        logger.info("[RuthValidationPgRepository] introduce_myself 진입 | request_data=%s", f"id={query.id} name={query.name!r}")
        return RuthValidationResponse(
            id=query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴",
        )

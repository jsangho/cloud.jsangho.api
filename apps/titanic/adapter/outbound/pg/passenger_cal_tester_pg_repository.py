from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository

logger = logging.getLogger("uvicorn.error")

class CalTesterPgRepository(CalTesterRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        logger.info("[CalTesterPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return CalTesterResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
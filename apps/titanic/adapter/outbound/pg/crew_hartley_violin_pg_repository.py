from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository

logger = logging.getLogger("uvicorn.error")

class HartleyViolinPgRepository(HartleyViolinRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        logger.info("[HartleyViolinPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return HartleyViolinResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
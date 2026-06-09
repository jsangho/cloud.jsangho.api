from __future__ import annotations
import logging



from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository

logger = logging.getLogger("uvicorn.error")


class HartleyViolinPgRepository(HartleyViolinRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HartleyViolinQuery) -> HartleyViolinResponse:
        logger.info("[HartleyViolinPgRepository] introduce_myself 진입 | request_data=%s", f"id={query.id} name={query.name!r}")
        return HartleyViolinResponse(
            id=query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴",
        )

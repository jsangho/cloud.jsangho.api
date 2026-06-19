from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoQuery, HendricksCeoResponse
from silicon_valley.app.ports.output.piper_hendricks_ceo_port import HendricksCeoPort


class HendricksCeoRepository(HendricksCeoPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HendricksCeoQuery) -> HendricksCeoResponse:
        return HendricksCeoResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

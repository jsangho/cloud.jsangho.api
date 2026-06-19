from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashQuery, DineshDashResponse
from silicon_valley.app.ports.output.piper_dinesh_dash_port import DineshDashPort


class DineshDashRepository(DineshDashPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: DineshDashQuery) -> DineshDashResponse:
        return DineshDashResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

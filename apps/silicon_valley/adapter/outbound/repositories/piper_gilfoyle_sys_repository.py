from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import GilfoyleSysQuery, GilfoyleSysResponse
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import GilfoyleSysPort


class GilfoyleSysRepository(GilfoyleSysPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: GilfoyleSysQuery) -> GilfoyleSysResponse:
        return GilfoyleSysResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

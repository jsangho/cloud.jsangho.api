from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import LAYER_LOG
from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel
from kayfabe.app.ports.output.result_repository import ResultRepository

logger = LAYER_LOG


class ResultPgRepository(ResultRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_ple_by_slug(self, slug: str) -> PleEventModel | None:
        result = await self.db.execute(select(PleEventModel).where(PleEventModel.slug == slug))
        return result.scalar_one_or_none()

    async def list_events_by_year(self, year: int) -> list[PleEventModel]:
        result = await self.db.execute(
            select(PleEventModel)
            .where(PleEventModel.year == year)
            .order_by(PleEventModel.month.asc())
        )
        return list(result.scalars().all())


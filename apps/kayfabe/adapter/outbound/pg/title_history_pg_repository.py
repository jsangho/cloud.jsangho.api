from __future__ import annotations

import asyncio

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from kayfabe.adapter.outbound.orm.title_history_orm import TitleAcquisitionModel
from kayfabe.app.ports.output.title_history_repository import (
    TitleAcquisitionRow,
    TitleHistoryRepository,
)
from kayfabe.app.services.competitor_roster import is_team_roster_name
from kayfabe.app.services.real_title_catalog import CATALOG_REVISION, individual_title_acquisitions

_sync_lock = asyncio.Lock()


class TitleHistoryPgRepository(TitleHistoryRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(TitleAcquisitionModel))
        return int(result.scalar_one())

    async def needs_real_resync(self) -> bool:
        if await self.count() == 0:
            return True
        result = await self.db.execute(
            select(TitleAcquisitionModel.id)
            .where(TitleAcquisitionModel.source != "real")
            .limit(1)
        )
        if result.scalar_one_or_none() is not None:
            return True
        revision = await self.db.execute(
            select(TitleAcquisitionModel.id)
            .where(TitleAcquisitionModel.source == f"real:{CATALOG_REVISION}")
            .limit(1)
        )
        if revision.scalar_one_or_none() is None:
            return True
        team_row = await self.db.execute(
            select(TitleAcquisitionModel.competitor_name).limit(500)
        )
        for (name,) in team_row.all():
            if is_team_roster_name(name):
                return True
        return False

    async def list_by_competitor(self, *, competitor_name: str) -> list[TitleAcquisitionRow]:
        result = await self.db.execute(
            select(TitleAcquisitionModel)
            .where(TitleAcquisitionModel.competitor_name == competitor_name)
            .order_by(TitleAcquisitionModel.id.asc())
        )
        return [
            TitleAcquisitionRow(
                belt_name=row.belt_name,
                won_at=row.won_at,
                won_at_slug=row.won_at_slug,
                match_key=row.match_key,
            )
            for row in result.scalars().all()
        ]

    async def sync_from_real_catalog(self) -> int:
        async with _sync_lock:
            await self.db.execute(delete(TitleAcquisitionModel))
            await self.db.flush()

            inserted = 0
            seen: set[tuple[str, str, str]] = set()
            source = f"real:{CATALOG_REVISION}"
            for competitor, reigns in individual_title_acquisitions().items():
                for belt_name, won_at in reigns:
                    key = (competitor, belt_name, won_at)
                    if key in seen:
                        continue
                    seen.add(key)
                    self.db.add(
                        TitleAcquisitionModel(
                            competitor_name=competitor,
                            belt_name=belt_name,
                            won_at=won_at,
                            won_at_slug=None,
                            match_key=None,
                            match_id=None,
                            source=source,
                        )
                    )
                    inserted += 1
            await self.db.flush()
            return inserted

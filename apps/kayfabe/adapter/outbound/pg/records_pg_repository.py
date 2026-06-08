from __future__ import annotations

import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from kayfabe.adapter.outbound.orm.ple_orm import PleEventModel, PleMatchModel
from kayfabe.app.ports.output.records_repository import RecordsRepository
from kayfabe.app.services.records_scoring import names_from_card_json, normalize_name

logger = LAYER_LOG

_CACHE_TTL_S = 20.0
_names_cache: tuple[float, list[str]] | None = None
_snapshots_cache: tuple[float, list[tuple[PleEventModel, PleMatchModel]]] | None = None


class RecordsPgRepository(RecordsRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_competitor_names(self) -> list[str]:
        global _names_cache
        now = time.monotonic()
        if _names_cache and (now - _names_cache[0]) < _CACHE_TTL_S:
            return _names_cache[1]

        logger.info("[RecordsPgRepository] list_competitor_names -> Neon")
        result = await self.db.execute(select(PleMatchModel.card_json))
        names: set[str] = set()
        for (card_json,) in result.all():
            if not card_json:
                continue
            for name in names_from_card_json(card_json):
                names.add(normalize_name(name))
        rows = sorted(names)
        logger.info("[RecordsPgRepository] list_competitor_names <- Neon count=%d", len(rows))
        _names_cache = (now, rows)
        return rows

    async def list_match_snapshots(self) -> list[tuple[PleEventModel, PleMatchModel]]:
        """
        Records는 예측/투표 집계가 필요 없어서, card_json + 결과 필드만 로드한다.
        (기존 PleInfo.get_board()는 predictions까지 로드하므로 records에서는 사용하지 않음)
        """
        global _snapshots_cache
        now = time.monotonic()
        if _snapshots_cache and (now - _snapshots_cache[0]) < _CACHE_TTL_S:
            return _snapshots_cache[1]

        logger.info("[RecordsPgRepository] list_match_snapshots -> Neon")
        stmt = (
            select(PleEventModel, PleMatchModel)
            .join(PleMatchModel, PleMatchModel.event_id == PleEventModel.id)
            .order_by(PleEventModel.month.asc(), PleMatchModel.sort_order.asc())
        )
        result = await self.db.execute(stmt)
        rows = list(result.all())
        logger.info("[RecordsPgRepository] list_match_snapshots <- Neon count=%d", len(rows))
        _snapshots_cache = (now, rows)
        return rows

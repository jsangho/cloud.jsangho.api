from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from friday13th.app.ports.output.murder_list_repository import MurderListRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class MurderListPgRepository(MurderListRepository):
    """Neon(Postgres) 프로필 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_id(self, user_id: int) -> UserModel | None:
        logger.info("[MurderListPgRepository] find_by_id -> Neon — db_id=%s", user_id)
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

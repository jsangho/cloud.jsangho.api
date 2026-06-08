from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import (
    format_preview_profile_request,
    format_preview_profile_response,
)
from friday13th.app.ports.output.murder_list_repository import MurderListRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class MurderListPgRepository(MurderListRepository):
    """Neon(Postgres) ?ë¡??ì¡°í ?´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_id(self, user_id: int) -> UserModel | None:
        logger.info(
            "[MurderListPgRepository] Repository?ì ë°ì? ?ë¡??ì¡°í ?ì²­ ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
            1,
        )
        preview_blocks = [format_preview_profile_request(1, user_id=user_id)]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info("[MurderListPgRepository] find_by_id -> Neon ??db_id=%s", user_id)
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalar_one_or_none()
        if user is not None:
            logger.info(
                "[MurderListPgRepository] Neon?ì ì¡°í???ì ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
                1,
            )
            preview_blocks = [
                format_preview_profile_response(1, user=user.to_log_dict())
            ]
            logger.info("\n%s", "\n".join(preview_blocks))
        return user

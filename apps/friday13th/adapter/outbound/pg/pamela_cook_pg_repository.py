from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import format_preview_login
from friday13th.app.ports.output.pamela_cook_repository import PamelaCookRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class PamelaCookPgRepository(PamelaCookRepository):
    """Neon(Postgres) ë¡ê·¸???´ë??"""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_login_id(self, login_id: str) -> UserModel | None:
        logger.info(
            "[PamelaCookPgRepository] Repository?ì ë°ì? ë¡ê·¸???ì²­ ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
            1,
        )
        preview_blocks = [format_preview_login(1, login_id=login_id)]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info(
            "[PamelaCookPgRepository] find_by_login_id -> Neon ??userId=%s", login_id
        )
        result = await self.db.execute(
            select(UserModel).where(UserModel.login_id == login_id)
        )
        return result.scalar_one_or_none()

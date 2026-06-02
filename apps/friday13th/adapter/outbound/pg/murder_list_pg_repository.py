from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import (
    format_preview_profile_request,
    format_preview_profile_response,
)
from friday13th.app.ports.output.murder_list_repository import MurderListRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class MurderListPgRepository(MurderListRepository):
    """Neon(Postgres) 프로필 조회 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_id(self, user_id: int) -> UserModel | None:
        logger.info(
            "[MurderListPgRepository] Repository에서 받은 프로필 조회 요청 미리보기 (상위 %s건)",
            1,
        )
        preview_blocks = [format_preview_profile_request(1, user_id=user_id)]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info("[MurderListPgRepository] find_by_id -> Neon — db_id=%s", user_id)
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalar_one_or_none()
        if user is not None:
            logger.info(
                "[MurderListPgRepository] Neon에서 조회된 회원 미리보기 (상위 %s건)",
                1,
            )
            preview_blocks = [
                format_preview_profile_response(1, user=user.to_log_dict())
            ]
            logger.info("\n%s", "\n".join(preview_blocks))
        return user

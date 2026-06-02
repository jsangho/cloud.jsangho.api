from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import format_preview_signup
from friday13th.app.ports.input.jason_mask_schema import JasonMaskSchema
from friday13th.app.ports.output.jason_mask_repository import JasonMaskRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class JasonMaskPgRepository(JasonMaskRepository):
    """Neon(Postgres) 회원가입 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_email(self, email: str) -> UserModel | None:
        logger.info("[JasonMaskPgRepository] find_by_email -> Neon — email=%s", email)
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalar_one_or_none()
        if user is None:
            logger.info(
                "[JasonMaskPgRepository] find_by_email <- Neon — email=%s, user=없음",
                email,
            )
        else:
            logger.info(
                "[JasonMaskPgRepository] find_by_email <- Neon — email=%s, user=%s",
                email,
                user.to_log_dict(),
            )
        return user

    async def find_by_login_id(self, login_id: str) -> UserModel | None:
        logger.info(
            "[JasonMaskPgRepository] find_by_login_id -> Neon — userId=%s", login_id
        )
        result = await self.db.execute(
            select(UserModel).where(UserModel.login_id == login_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            logger.info(
                "[JasonMaskPgRepository] find_by_login_id <- Neon — userId=%s, user=없음",
                login_id,
            )
        else:
            logger.info(
                "[JasonMaskPgRepository] find_by_login_id <- Neon — userId=%s, user=%s",
                login_id,
                user.to_log_dict(),
            )
        return user

    async def save_user(
        self, user_schema: JasonMaskSchema, password_hash: str
    ) -> UserModel:
        logger.info(
            "[JasonMaskPgRepository] Repository에서 받은 회원가입 스키마 미리보기 (상위 %s건)",
            1,
        )
        preview_blocks = [
            format_preview_signup(
                1,
                login_id=user_schema.login_id,
                nickname=user_schema.nickname,
                email=user_schema.email,
                role=user_schema.role,
            )
        ]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info(
            "[JasonMaskPgRepository] save_user -> Neon — userId=%s, email=%s",
            user_schema.login_id,
            user_schema.email,
        )
        user = UserModel(
            login_id=user_schema.login_id,
            nickname=user_schema.nickname,
            email=user_schema.email,
            password_hash=password_hash,
            role=user_schema.role,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        logger.info(
            "[JasonMaskPgRepository] save_user <- Neon — userId=%s, db_id=%s",
            user_schema.login_id,
            user.id,
        )
        return user

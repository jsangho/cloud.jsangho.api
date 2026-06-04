from __future__ import annotations

from fastapi import HTTPException

from core.matrix.oracle_database import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import format_preview_signup
from friday13th.app.ports.input.jason_mask_schema import JasonMaskSchema
from friday13th.app.ports.input.jason_mask_use_case import JasonMaskUseCase
from friday13th.app.ports.output.jason_mask_repository import JasonMaskRepository
from friday13th.domain.services.password import hash_password

logger = LAYER_LOG


class JasonMaskInteractor(JasonMaskUseCase):
    """?ìê°??? ì¤ì¼?´ì¤ êµ¬íì²?"""

    def __init__(self, repository: JasonMaskRepository) -> None:
        self._repository = repository

    async def save_user(self, *, user_schema: JasonMaskSchema) -> None:
        logger.info(
            "[JasonMaskInteractor] ?¼ì°?°ì??? ì¤ì¼?´ì¤ë¡???²¨ì§??ìê°???¤í¤ë§?ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
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
            "[JasonMaskInteractor] save_user -> Repository ??userId=%s, email=%s",
            user_schema.login_id,
            user_schema.email,
        )
        if user_schema.password != user_schema.password_confirm:
            raise HTTPException(
                status_code=400,
                detail="ë¹ë?ë²í¸? ë¹ë?ë²í¸ ?ì¸???¼ì¹?ì? ?ìµ?ë¤.",
            )

        if await self._repository.find_by_email(user_schema.email):
            raise HTTPException(status_code=409, detail="?´ë? ê°?
ë ?´ë©?¼ì
?ë¤.")

        if await self._repository.find_by_login_id(user_schema.login_id):
            raise HTTPException(status_code=409, detail="?´ë? ?¬ì© ì¤ì¸ ID?
ë??")

        password_hash = hash_password(user_schema.password)
        user = await self._repository.save_user(user_schema, password_hash)
        logger.info(
            "[JasonMaskInteractor] save_user <- Repository ??userId=%s, db_id=%s",
            user_schema.login_id,
            user.id,
        )

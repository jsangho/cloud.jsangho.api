from __future__ import annotations

import asyncio

from fastapi import HTTPException

from core.matrix.oracle_database import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import format_preview_login
from friday13th.app.ports.input.pamela_cook_use_case import PamelaCookUseCase
from friday13th.app.ports.output.pamela_cook_repository import PamelaCookRepository
from friday13th.domain.entities.user_model import UserModel
from friday13th.domain.services.password import verify_password

logger = LAYER_LOG


class PamelaCookInteractor(PamelaCookUseCase):
    """ë¡ê·¸??? ì¤ì¼?´ì¤ êµ¬íì²?"""

    def __init__(self, repository: PamelaCookRepository) -> None:
        self._repository = repository

    async def login_user(self, *, login_id: str, password: str) -> UserModel:
        logger.info(
            "[PamelaCookInteractor] ?¼ì°?°ì??? ì¤ì¼?´ì¤ë¡???²¨ì§?ë¡ê·¸???ì²­ ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
            1,
        )
        preview_blocks = [format_preview_login(1, login_id=login_id)]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info("[PamelaCookInteractor] login_user -> Repository ??userId=%s", login_id)
        user = await self._repository.find_by_login_id(login_id)
        password_ok = await asyncio.to_thread(
            verify_password, password, user.password_hash if user else ""
        )
        if user is None or not password_ok:
            logger.info(
                "[PamelaCookInteractor] login_user <- Repository ??userId=%s, ?¸ì¦?¤í¨",
                login_id,
            )
            raise HTTPException(
                status_code=401,
                detail="ID ?ë ë¹ë?ë²í¸ê° ?¬ë°ë¥´ì? ?ìµ?ë¤.",
            )
        logger.info(
            "[PamelaCookInteractor] login_user <- Repository ??userId=%s",
            login_id,
        )
        return user

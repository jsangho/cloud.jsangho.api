from __future__ import annotations

from fastapi import HTTPException

from core.matrix.oracle_database import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import (
    format_preview_profile_request,
    format_preview_profile_response,
)
from friday13th.app.ports.input.murder_list_use_case import MurderListUseCase
from friday13th.app.ports.output.murder_list_repository import MurderListRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class MurderListInteractor(MurderListUseCase):
    """?ì ?ë¡??ì¡°í ? ì¤ì¼?´ì¤ êµ¬íì²?"""

    def __init__(self, repository: MurderListRepository) -> None:
        self._repository = repository

    async def get_user_by_id(self, *, user_id: int) -> UserModel:
        logger.info(
            "[MurderListInteractor] ?¼ì°?°ì??? ì¤ì¼?´ì¤ë¡???²¨ì§??ë¡??ì¡°í ?ì²­ ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
            1,
        )
        preview_blocks = [format_preview_profile_request(1, user_id=user_id)]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info("[MurderListInteractor] get_user_by_id -> Repository ??db_id=%s", user_id)
        user = await self._repository.find_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="?ì??ì°¾ì ???ìµ?ë¤.")
        logger.info(
            "[MurderListInteractor] Repository?ì ì¡°í???ì ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
            1,
        )
        preview_blocks = [
            format_preview_profile_response(1, user=user.to_log_dict())
        ]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info(
            "[MurderListInteractor] get_user_by_id <- Repository ??db_id=%s",
            user_id,
        )
        return user

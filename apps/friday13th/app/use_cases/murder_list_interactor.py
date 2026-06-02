from __future__ import annotations

from fastapi import HTTPException

from core.database import LAYER_LOG
from friday13th.adapter.inbound.api.schemas.friday13th_preview import (
    format_preview_profile_request,
    format_preview_profile_response,
)
from friday13th.app.ports.input.murder_list_use_case import MurderListUseCase
from friday13th.app.ports.output.murder_list_repository import MurderListRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class MurderListInteractor(MurderListUseCase):
    """회원 프로필 조회 유스케이스 구현체."""

    def __init__(self, repository: MurderListRepository) -> None:
        self._repository = repository

    async def get_user_by_id(self, *, user_id: int) -> UserModel:
        logger.info(
            "[MurderListInteractor] 라우터에서 유스케이스로 옮겨진 프로필 조회 요청 미리보기 (상위 %s건)",
            1,
        )
        preview_blocks = [format_preview_profile_request(1, user_id=user_id)]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info("[MurderListInteractor] get_user_by_id -> Repository — db_id=%s", user_id)
        user = await self._repository.find_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
        logger.info(
            "[MurderListInteractor] Repository에서 조회된 회원 미리보기 (상위 %s건)",
            1,
        )
        preview_blocks = [
            format_preview_profile_response(1, user=user.to_log_dict())
        ]
        logger.info("\n%s", "\n".join(preview_blocks))
        logger.info(
            "[MurderListInteractor] get_user_by_id <- Repository — db_id=%s",
            user_id,
        )
        return user

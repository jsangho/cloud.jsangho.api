from __future__ import annotations

from fastapi import HTTPException

from core.database import LAYER_LOG
from friday13th.app.ports.input.murder_list_use_case import MurderListUseCase
from friday13th.app.ports.output.murder_list_repository import MurderListRepository
from friday13th.domain.entities.user_model import UserModel

logger = LAYER_LOG


class MurderListInteractor(MurderListUseCase):
    """회원 프로필 조회 유스케이스 구현체."""

    def __init__(self, repository: MurderListRepository) -> None:
        self._repository = repository

    async def get_user_by_id(self, *, user_id: int) -> UserModel:
        logger.info("[MurderListInteractor] get_user_by_id -> Repository — db_id=%s", user_id)
        user = await self._repository.find_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
        logger.info(
            "[MurderListInteractor] get_user_by_id <- Repository — db_id=%s",
            user_id,
        )
        return user

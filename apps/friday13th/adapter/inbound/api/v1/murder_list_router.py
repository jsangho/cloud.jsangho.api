from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from friday13th.adapter.inbound.api.schemas.friday13th_preview import (
    format_preview_profile_request,
)
from friday13th.app.ports.input.murder_list_use_case import MurderListUseCase
from friday13th.domain.value_objects.role import UserRole

logger = logging.getLogger("uvicorn.error")

murder_list_router = APIRouter(prefix="/murder-list", tags=["murder-list"])


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="userId")
    login_id: str = Field(alias="loginId")
    nickname: str
    email: str
    role: UserRole


def get_murder_list_use_case(db: AsyncSession = Depends(get_db)) -> MurderListUseCase:
    from friday13th.adapter.outbound.pg.murder_list_pg_repository import MurderListPgRepository
    from friday13th.app.use_cases.murder_list_interactor import MurderListInteractor

    return MurderListInteractor(MurderListPgRepository(db))


@murder_list_router.get(
    "/users/{user_id}",
    response_model=UserProfileResponse,
    response_model_by_alias=True,
)
async def get_user_profile(
    user_id: int,
    use_case: MurderListUseCase = Depends(get_murder_list_use_case),
):
    logger.info(
        "[Friday13th MurderList ?¼ì°?? ?ë¡??ì¡°í ?ì²­ ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
        1,
    )
    preview_blocks = [format_preview_profile_request(1, user_id=user_id)]
    logger.info("\n%s", "\n".join(preview_blocks))
    user = await use_case.get_user_by_id(user_id=user_id)
    return UserProfileResponse(
        id=user.id,
        login_id=user.login_id or "",
        nickname=user.nickname,
        email=user.email,
        role=UserRole(user.role),
    )

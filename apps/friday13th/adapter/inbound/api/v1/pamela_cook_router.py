from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from friday13th.adapter.inbound.api.schemas.friday13th_preview import format_preview_login
from friday13th.app.ports.input.pamela_cook_use_case import PamelaCookUseCase
from friday13th.domain.value_objects.role import UserRole

logger = logging.getLogger("uvicorn.error")

pamela_cook_router = APIRouter(prefix="/pamela-cook", tags=["pamela-cook"])


class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(..., alias="userId", min_length=1, description="ë¡ê·¸??ID")
    password: str = Field(..., min_length=1, description="ë¡ê·¸??ë¹ë?ë²í¸")


class LoginResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str
    id: int = Field(alias="userId", description="?ì DB id (?ì¸¡Â·?ì ?°ë)")
    login_id: str = Field(alias="loginId", description="ë¡ê·¸??ID")
    nickname: str
    email: str
    role: UserRole


def get_pamela_cook_use_case(db: AsyncSession = Depends(get_db)) -> PamelaCookUseCase:
    from friday13th.adapter.outbound.pg.pamela_cook_pg_repository import PamelaCookPgRepository
    from friday13th.app.use_cases.pamela_cook_interactor import PamelaCookInteractor

    return PamelaCookInteractor(PamelaCookPgRepository(db))


@pamela_cook_router.post("/login", response_model=LoginResponse, response_model_by_alias=True)
async def login(
    req: LoginRequest,
    use_case: PamelaCookUseCase = Depends(get_pamela_cook_use_case),
):
    login_id = req.user_id.strip()
    logger.info(
        "[Friday13th PamelaCook ?¼ì°?? ë¡ê·¸???ì²­ ë¯¸ë¦¬ë³´ê¸° (?ì %sê±?",
        1,
    )
    preview_blocks = [format_preview_login(1, login_id=login_id)]
    logger.info("\n%s", "\n".join(preview_blocks))
    user = await use_case.login_user(login_id=login_id, password=req.password)
    return LoginResponse(
        message="ë¡ê·¸?¸ë?ìµ?ë¤.",
        id=user.id,
        login_id=user.login_id or login_id,
        nickname=user.nickname,
        email=user.email,
        role=UserRole(user.role),
    )

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from friday13th.app.ports.input.jason_mask_schema import JasonMaskSchema
from friday13th.app.ports.input.jason_mask_use_case import JasonMaskUseCase
from friday13th.domain.value_objects.role import UserRole

logger = logging.getLogger("uvicorn.error")

jason_mask_router = APIRouter(prefix="/friday13th/jason-mask",tags=["jason-mask"])


class SignupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(..., alias="userId", min_length=1, description="회원가입 ID")
    nickname: str = Field(..., min_length=1, description="회원가입 닉네임")
    email: str = Field(..., min_length=1, description="회원가입 이메일")
    password: str = Field(..., min_length=1, description="회원가입 비밀번호")
    password_confirm: str = Field(
        ...,
        alias="passwordConfirm",
        min_length=1,
        description="회원가입 비밀번호 확인",
    )


class SignupResponse(BaseModel):
    message: str
    nickname: str
    email: str
    role: UserRole


def get_jason_mask_use_case(db: AsyncSession = Depends(get_db)) -> JasonMaskUseCase:
    from friday13th.adapter.outbound.pg.jason_mask_pg_repository import JasonMaskPgRepository
    from friday13th.app.use_cases.jason_mask_interactor import JasonMaskInteractor

    return JasonMaskInteractor(JasonMaskPgRepository(db))


@jason_mask_router.post("/signup", response_model=SignupResponse)
async def signup(
    req: SignupRequest,
    use_case: JasonMaskUseCase = Depends(get_jason_mask_use_case),
):
    logger.info("[API] POST /signup — userId=%s", req.user_id)
    user_schema = JasonMaskSchema(
        login_id=req.user_id.strip(),
        nickname=req.nickname,
        email=req.email,
        password=req.password,
        password_confirm=req.password_confirm,
        role=UserRole.USER,
    )
    await use_case.save_user(user_schema=user_schema)
    return SignupResponse(
        message="회원가입이 완료되었습니다.",
        nickname=req.nickname,
        email=req.email,
        role=UserRole.USER,
    )

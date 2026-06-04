from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from friday13th.adapter.inbound.api.schemas.friday13th_preview import (
    format_preview_signup,
)
from friday13th.app.ports.input.jason_mask_schema import JasonMaskSchema
from friday13th.app.ports.input.jason_mask_use_case import JasonMaskUseCase
from friday13th.domain.value_objects.role import UserRole

logger = logging.getLogger("uvicorn.error")

jason_mask_router = APIRouter(prefix="/jason-mask", tags=["jason-mask"])


class SignupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(..., alias="userId", min_length=1, description="???? ID")
    nickname: str = Field(..., min_length=1, description="???? ???")
    email: str = Field(..., min_length=1, description="???? ???")
    password: str = Field(..., min_length=1, description="???? ????")
    password_confirm: str = Field(
        ...,
        alias="passwordConfirm",
        min_length=1,
        description="???? ???? ??",
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
    logger.info(
        "[Friday13th JasonMask ???] ???? ?? ???? (?? %s?)",
        1,
    )
    preview_blocks = [
        format_preview_signup(
            1,
            login_id=req.user_id.strip(),
            nickname=req.nickname,
            email=req.email,
            role=UserRole.USER,
        )
    ]
    logger.info("\n%s", "\n".join(preview_blocks))
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
        message="????? ???????.",
        nickname=req.nickname,
        email=req.email,
        role=UserRole.USER,
    )

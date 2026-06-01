from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.domain.entities.user_model import UserModel


class PamelaCookUseCase(ABC):
    """`/friday13th/pamela-cook/*` inbound(pamela_cook_router)가 호출하는 입력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def login_user(self, *, login_id: str, password: str) -> UserModel:
        """로그인 (`POST /login`)."""
        ...

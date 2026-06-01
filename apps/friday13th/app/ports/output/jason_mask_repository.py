from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.app.ports.input.jason_mask_schema import JasonMaskSchema
from friday13th.domain.entities.user_model import UserModel


class JasonMaskRepository(ABC):
    """회원가입 데이터를 영속화하는 출력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def find_by_email(self, email: str) -> UserModel | None:
        """이메일 중복 확인."""
        ...

    @abstractmethod
    async def find_by_login_id(self, login_id: str) -> UserModel | None:
        """로그인 ID 중복 확인."""
        ...

    @abstractmethod
    async def save_user(
        self, user_schema: JasonMaskSchema, password_hash: str
    ) -> UserModel:
        """회원가입 저장 (`save_user`)."""
        ...

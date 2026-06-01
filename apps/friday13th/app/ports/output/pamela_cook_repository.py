from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.domain.entities.user_model import UserModel


class PamelaCookRepository(ABC):
    """로그인 데이터를 제공하는 출력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def find_by_login_id(self, login_id: str) -> UserModel | None:
        ...

from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.domain.entities.user_model import UserModel


class MurderListRepository(ABC):
    """프로필 조회 데이터를 제공하는 출력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def find_by_id(self, user_id: int) -> UserModel | None:
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JamesRepository(ABC):
    """James 업로드 데이터를 영속화하는 출력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def save_fileupload_rows(
        self, *, filename: str, rows: list[dict[str, Any]]
    ) -> int:
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JamesDirectorRepository(ABC):
    """James Director 업로드 데이터 영속화 출력 포트."""

    @abstractmethod
    async def save_fileupload_rows(
        self, *, filename: str, rows: list[dict[str, Any]]
    ) -> int:
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JamesDirectorUseCase(ABC):
    """`/titanic/james-director/*` inbound(james_director_router) 입력 포트."""

    @abstractmethod
    async def fileupload(
        self,
        *,
        filename: str,
        rows: list[dict[str, Any]],
    ) -> dict[str, int]:
        """CSV 업로드 (`POST /fileupload`)."""
        ...

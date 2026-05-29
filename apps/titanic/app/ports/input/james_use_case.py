from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.ports.output.james_repository import JamesRepository


class JamesUseCase(ABC):
    """`/titanic/james/*` inbound가 호출하는 입력 포트 (구현·로그 없음, ABC만)."""

    @abstractmethod
    async def fileupload(
        self,
        *,
        repository: JamesRepository,
        filename: str,
        rows: list[dict[str, Any]],
    ) -> dict[str, int]:
        ...

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackTrainerRepository(ABC):
    """Jack 스케치 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_trainer(self) -> dict[str, Any]:
        ...

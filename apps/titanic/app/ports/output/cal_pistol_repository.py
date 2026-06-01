from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CalPistolRepository(ABC):
    """Cal 권총 조회 데이터 출력 포트."""

    @abstractmethod
    async def get_pistol(self) -> dict[str, Any]:
        ...

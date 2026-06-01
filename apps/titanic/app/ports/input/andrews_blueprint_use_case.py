from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AndrewsBlueprintUseCase(ABC):
    """`/titanic/andrews/*` inbound(andrews_blueprint_router) 입력 포트."""

    @abstractmethod
    async def get_blueprint(self) -> dict[str, Any]:
        """설계도 조회 (`GET /blueprint`)."""
        ...

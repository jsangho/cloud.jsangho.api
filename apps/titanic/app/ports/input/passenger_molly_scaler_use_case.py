from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MollyScalerUseCase(ABC):
    """`/titanic/cal/*` inbound(molly_scaler_router) 입력 포트."""

    @abstractmethod
    async def get_scaler(self) -> dict[str, Any]:
        """권총 조회 (`GET /pistol`)."""
        ...

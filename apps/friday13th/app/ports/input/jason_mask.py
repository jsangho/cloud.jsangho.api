from __future__ import annotations

from abc import ABC, abstractmethod

from friday13th.app.ports.input.jason_mask_schema import JasonMaskSchema


class JasonMaskUseCase(ABC):
    @abstractmethod
    async def save_user(self, *, user_schema: JasonMaskSchema) -> None:
        ...

from __future__ import annotations

from abc import ABC, abstractmethod

from manager.app.dtos.telegram_dto import TelegramQuery, TelegramResponse


class TelegramRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: TelegramQuery) -> TelegramResponse: ...

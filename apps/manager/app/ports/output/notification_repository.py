from __future__ import annotations

from abc import ABC, abstractmethod

from manager.app.dtos.notification_dto import NotificationDto


class NotificationRepository(ABC):
    @abstractmethod
    async def save(self, dto: NotificationDto, status: str) -> int: ...

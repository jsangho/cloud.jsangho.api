from __future__ import annotations

from abc import ABC, abstractmethod

from manager.app.dtos.received_dto import ReceivedCommand, ReceivedItem


class ReceivedRepository(ABC):
    @abstractmethod
    async def save(self, cmd: ReceivedCommand) -> int: ...

    @abstractmethod
    async def list_all(self) -> list[ReceivedItem]: ...

    @abstractmethod
    async def mark_read(self, item_id: int) -> None: ...

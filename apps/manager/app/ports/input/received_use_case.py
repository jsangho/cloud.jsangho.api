from __future__ import annotations

from abc import ABC, abstractmethod

from manager.app.dtos.received_dto import ReceivedCommand, ReceivedItem


class ReceivedUseCase(ABC):
    @abstractmethod
    async def receive(self, cmd: ReceivedCommand) -> dict[str, int]: ...

    @abstractmethod
    async def list_inbox(self) -> list[ReceivedItem]: ...

    @abstractmethod
    async def mark_read(self, item_id: int) -> None: ...

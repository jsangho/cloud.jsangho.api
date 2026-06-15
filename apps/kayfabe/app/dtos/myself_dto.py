from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class MyselfQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MyselfResponse:
    id: int
    name: str


class MyselfRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: MyselfQuery) -> MyselfResponse: ...


class MyselfUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: MyselfQuery) -> MyselfResponse: ...

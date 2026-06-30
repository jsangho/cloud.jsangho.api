from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramQuery:
    id: int
    name: str


@dataclass
class TelegramResponse:
    id: int
    name: str
    description: str

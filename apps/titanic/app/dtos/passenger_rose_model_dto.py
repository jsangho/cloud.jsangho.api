from dataclasses import dataclass


@dataclass(frozen=True)
class RoseModelQuery:
    id: int
    name: str


@dataclass(frozen=True)
class RoseModelResponse:
    id: int
    name: str


@dataclass
class BookingCommand:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str

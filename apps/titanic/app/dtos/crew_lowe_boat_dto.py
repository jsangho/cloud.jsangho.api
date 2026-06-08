from dataclasses import dataclass


@dataclass
class LoweBoatQuery:
    id: int
    name: str
    memo: str


@dataclass
class LoweBoatResponse:
    id: int
    name: str
    memo: str

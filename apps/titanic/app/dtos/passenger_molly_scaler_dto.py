from dataclasses import dataclass


@dataclass
class MollyScalerQuery:
    id: int
    name: str
    memo: str


@dataclass
class MollyScalerResponse:
    id: int
    name: str
    memo: str

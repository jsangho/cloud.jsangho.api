"""{stem} API 스키마."""

from pydantic import BaseModel


class LoweBoatSchema(BaseModel):
    id: int = 1
    name: str = "Harold Lowe"
    memo: str = "구명보트 배정 분석"

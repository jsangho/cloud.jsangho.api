"""{stem} API 스키마."""

from pydantic import BaseModel


class IsidorCoupleSchema(BaseModel):
    id: int = 1
    name: str = "Isidor & Ida Straus"
    memo: str = "부부 승객 특성 분석"

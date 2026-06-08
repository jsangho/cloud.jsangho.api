"""{stem} API 스키마."""

from pydantic import BaseModel


class SmithCaptainSchema(BaseModel):
    id: int = 1
    name: str = "Edward Smith"
    memo: str = "선장, 승선 계층 분석"

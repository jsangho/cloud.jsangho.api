"""{stem} API 스키마."""

from pydantic import BaseModel


class HartleyViolinSchema(BaseModel):
    id: int = 1
    name: str = "Wallace Hartley"
    memo: str = "밴드마스터, 생존 통계"

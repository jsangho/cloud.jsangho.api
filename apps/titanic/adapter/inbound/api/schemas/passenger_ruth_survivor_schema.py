"""{stem} API 스키마."""

from pydantic import BaseModel


class RuthSurvivorSchema(BaseModel):
    id: int = 1
    name: str = "Ruth DeWitt Bukater"
    memo: str = "생존자 라벨 검증"

"""{stem} API 스키마."""

from pydantic import BaseModel


class RoseModelSchema(BaseModel):
    id: int = 1
    name: str = "Rose DeWitt Bukater"
    memo: str = "생존 예측 모델 검증"

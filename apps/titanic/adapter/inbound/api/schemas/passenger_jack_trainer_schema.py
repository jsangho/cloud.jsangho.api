"""{stem} API 스키마."""

from pydantic import BaseModel


class JackTrainerSchema(BaseModel):
    id: int = 1
    name: str = "Jack Dawson"
    memo: str = "3등실 승객, 생존 예측 학습"

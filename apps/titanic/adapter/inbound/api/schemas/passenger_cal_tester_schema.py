"""{stem} API 스키마."""

from pydantic import BaseModel


class CalTesterSchema(BaseModel):
    id: int = 1
    name: str = "Caledon Hockley"
    memo: str = "타이타닉 일등실 승객, 생존 분류 검증"

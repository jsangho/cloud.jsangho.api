"""{stem} API 스키마."""

from pydantic import BaseModel


class AndrewsArchitectSchema(BaseModel):
    id: int = 1
    name: str = "Thomas Andrews"
    memo: str = "선박 설계·구조 특성"

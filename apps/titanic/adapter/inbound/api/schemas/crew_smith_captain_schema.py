from typing import Literal

from pydantic import BaseModel, Field


class ChatMessageSchema(BaseModel):
    role: Literal["user", "assistant"]
    text: str = Field(..., min_length=1)


class ChatSchema(BaseModel):
    messages: list[ChatMessageSchema] = Field(..., min_length=1)
    stream: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {"role": "user", "text": "타이타닉 총 탑승객은 몇 명이야?"},
                ],
                "stream": True,
            }
        }
    }


class SmithCaptainChatResponseSchema(BaseModel):
    reply: str


class SmithCaptainSchema(BaseModel):
    id: int = Field(0, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Edward Smith",
            }
        }
    }

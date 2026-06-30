from pydantic import BaseModel


class TelegramMyselfSchema(BaseModel):
    id: int = 3
    name: str = "Telegram Manager"

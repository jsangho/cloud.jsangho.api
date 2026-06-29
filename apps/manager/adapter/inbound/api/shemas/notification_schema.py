from pydantic import BaseModel


class NotifyRequest(BaseModel):
    to: str

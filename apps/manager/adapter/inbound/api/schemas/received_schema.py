from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ReceiveRequest(BaseModel):
    from_email: str
    from_name: str = ""
    to_email: str = ""
    subject: str = ""
    body: str = ""
    message_id: str = ""


class ReceivedResponse(BaseModel):
    id: int
    from_email: str
    from_name: str
    to_email: str
    subject: str
    body: str
    message_id: str
    received_at: datetime
    is_read: bool

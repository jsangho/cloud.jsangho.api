from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReceivedCommand:
    from_email: str
    from_name: str = ""
    to_email: str = ""
    subject: str = ""
    body: str = ""
    message_id: str = ""


@dataclass
class ReceivedItem:
    id: int
    from_email: str
    from_name: str
    to_email: str
    subject: str
    body: str
    message_id: str
    received_at: datetime
    is_read: bool

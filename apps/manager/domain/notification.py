from dataclasses import dataclass


@dataclass
class EmailNotification:
    to: str
    subject: str
    body: str

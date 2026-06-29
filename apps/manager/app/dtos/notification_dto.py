from dataclasses import dataclass


@dataclass
class NotificationDto:
    to: str
    subject: str
    body: str

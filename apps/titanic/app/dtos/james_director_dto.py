from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PersonCommand:
    """Person 테이블 업로드용 DTO."""

    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass
class BookingCommand:
    """Booking·승선 항구 코드 업로드용 DTO."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str

from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.matrix.oracle_database import Base


class PersonOrm(Base):
    """James Director `PersonCommand` → Neon `titanic_persons`."""

    __tablename__ = "titanic_persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False, index=True
    )
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(10), nullable=True)
    age: Mapped[float | None] = mapped_column(Float, nullable=True)
    sib_sp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parch: Mapped[int | None] = mapped_column(Integer, nullable=True)
    survived: Mapped[int | None] = mapped_column(Integer, nullable=True)

    bookings: Mapped[list["BookingOrm"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan",
    )

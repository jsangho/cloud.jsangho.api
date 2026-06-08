from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.matrix.grid_oracle_database_manager import Base
from titanic.adapter.outbound.orm.person_orm import PersonOrm


class BookingOrm(Base):
    """James Director `BookingCommand` → Neon `titanic_bookings`."""

    __tablename__ = "titanic_bookings"
    __table_args__ = (UniqueConstraint("person_id", name="uq_titanic_bookings_person_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("titanic_persons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    pclass: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String(64), nullable=True)
    fare: Mapped[float | None] = mapped_column(Float, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String(32), nullable=True)
    embarked: Mapped[str | None] = mapped_column(String(1), nullable=True)

    person: Mapped[PersonOrm] = relationship(back_populates="bookings")

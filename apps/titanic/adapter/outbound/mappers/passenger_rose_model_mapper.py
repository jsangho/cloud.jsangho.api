"""passenger_rose_model 슬라이스 Mapper — Booking Entity ↔ RoseModelOrm."""

from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm
from titanic.domain.entities.passenger_rose_model_entity import Booking


class RoseModelMapper:
    @staticmethod
    def to_entity(orm: RoseModelOrm) -> Booking:
        return Booking.create(
            id=orm.id,
            person_id=orm.person_id,
            pclass=orm.pclass,
            ticket=orm.ticket,
            fare=orm.fare,
            cabin=orm.cabin,
            embarked=orm.embarked,
        )

    @staticmethod
    def to_orm(entity: Booking) -> RoseModelOrm:
        return RoseModelOrm(
            id=entity.id,
            person_id=entity.person_id,
            pclass=entity.pclass,
            ticket=entity.ticket,
            fare=entity.fare,
            cabin=entity.cabin,
            embarked=entity.embarked,
        )

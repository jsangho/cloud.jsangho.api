"""passenger_jack_trainer 슬라이스 Mapper — Passenger Entity ↔ JackTrainerOrm."""

from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import Passenger


class JackTrainerMapper:
    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> Passenger:
        return Passenger.create(
            id=orm.id,
            passenger_id=orm.passenger_id,
            name=orm.name,
            gender=orm.gender,
            age=orm.age,
            sib_sp=orm.sib_sp,
            parch=orm.parch,
            survived=orm.survived,
        )

    @staticmethod
    def to_orm(entity: Passenger) -> JackTrainerOrm:
        sib_sp: str | None = None
        parch: str | None = None
        if entity.family_info is not None:
            sib_sp = str(entity.family_info.sib_sp)
            parch = str(entity.family_info.parch)

        return JackTrainerOrm(
            id=entity.id,
            passenger_id=str(entity.passenger_id) if entity.passenger_id else None,
            name=str(entity.name) if entity.name else None,
            gender=str(entity.gender) if entity.gender else None,
            age=str(entity.age) if entity.age else None,
            sib_sp=sib_sp,
            parch=parch,
            survived=str(entity.survived) if entity.survived else None,
        )

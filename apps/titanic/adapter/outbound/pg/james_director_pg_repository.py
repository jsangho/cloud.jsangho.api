from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import james_director_upload_info
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository
from titanic.domain.entities.passenger_model import PassengerModel

_SRC = Path(__file__).name


def _opt_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def _opt_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _row_to_fields(row: dict[str, Any]) -> dict[str, Any]:
    gender = row.get("gender") or row.get("Sex")
    return {
        "passenger_id": int(row["PassengerId"]),
        "survived": _opt_int(row.get("Survived")),
        "pclass": _opt_int(row.get("Pclass")),
        "name": row.get("Name") or None,
        "sex": gender or None,
        "age": _opt_float(row.get("Age")),
        "sibsp": _opt_int(row.get("SibSp")),
        "parch": _opt_int(row.get("Parch")),
        "ticket": row.get("Ticket") or None,
        "fare": _opt_float(row.get("Fare")),
        "cabin": row.get("Cabin") or None,
        "embarked": row.get("Embarked") or None,
    }


class JamesDirectorPgRepository(JamesDirectorRepository):
    """Neon(Postgres) `titanic_passengers` 업로드 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save_fileupload_rows(
        self, *, filename: str, rows: list[dict[str, Any]]
    ) -> int:
        james_director_upload_info(
            _SRC, "file=%s rows=%s -> Neon", filename, len(rows)
        )
        saved = 0
        for row in rows:
            fields = _row_to_fields(row)
            passenger_id = fields["passenger_id"]
            result = await self._db.execute(
                select(PassengerModel).where(
                    PassengerModel.passenger_id == passenger_id
                )
            )
            entity = result.scalar_one_or_none()
            if entity is None:
                self._db.add(PassengerModel(**fields))
                saved += 1
            else:
                for key, value in fields.items():
                    setattr(entity, key, value)
        await self._db.flush()
        james_director_upload_info(
            _SRC, "file=%s saved=%s -> Neon", filename, saved
        )
        return len(rows)

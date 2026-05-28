from __future__ import annotations

from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from titanic.app.use_cases.titanic_models import PassengerModel

logger = LAYER_LOG
_SRC = Path(__file__).name


def _parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None


def _parse_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def _row_to_passenger(row: dict[str, Any]) -> PassengerModel:
    """CSV row(dict) → Neon ORM. `Sex`는 inbound에서 `gender`로 변환된 값을 사용."""
    return PassengerModel(
        passenger_id=_parse_int(row.get("PassengerId")) or 0,
        survived=_parse_int(row.get("Survived")),
        pclass=_parse_int(row.get("Pclass")),
        name=(row.get("Name") or None),
        sex=(row.get("gender") or None),
        age=_parse_float(row.get("Age")),
        sibsp=_parse_int(row.get("SibSp")),
        parch=_parse_int(row.get("Parch")),
        ticket=(row.get("Ticket") or None),
        fare=_parse_float(row.get("Fare")),
        cabin=(row.get("Cabin") or None),
        embarked=(row.get("Embarked") or None),
    )


class JamesPgRepository:
    """Postgres(Neon) 저장 어댑터."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def save_fileupload_rows(
        self, *, filename: str, rows: list[dict[str, Any]]
    ) -> int:
        if not rows:
            return 0

        logger.info("[JamesUpload][%s] file=%s -> pg_adapter(neon) flush(start)", _SRC, filename)
        for row in rows:
            self.db.add(_row_to_passenger(row))
        await self.db.flush()
        logger.info(
            "[JamesUpload][%s] file=%s -> pg_adapter(neon) flush(done) inserted=%s",
            _SRC,
            filename,
            len(rows),
        )
        return len(rows)

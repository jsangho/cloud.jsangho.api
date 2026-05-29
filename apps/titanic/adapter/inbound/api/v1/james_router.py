from __future__ import annotations

import csv
import io
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db, james_upload_info
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository

_SRC = Path(__file__).name

router = APIRouter(prefix="/titanic/james", tags=["james"])

_REQUIRED_COLUMNS = (
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
)


def _decode_csv_bytes(raw: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    raise HTTPException(status_code=400, detail="CSV 인코딩을 해석할 수 없습니다. UTF-8로 저장해 주세요.")


def get_james_use_case() -> JamesUseCase:
    from titanic.app.use_cases.james_command import JamesCommand

    return JamesCommand()


def get_james_repository(db: AsyncSession = Depends(get_db)) -> JamesRepository:
    from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository

    return JamesPgRepository(db)


@router.post("/fileupload")
async def upload_titanic_csv(
    file: UploadFile = File(...),
    use_case: JamesUseCase = Depends(get_james_use_case),
    repository: JamesRepository = Depends(get_james_repository),
):
    filename = (file.filename or "").strip() or "<unknown>"
    if not (file.filename or "").lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일(.csv)만 업로드할 수 있습니다.")

    raw = await file.read()
    text = _decode_csv_bytes(raw)

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

    missing = [c for c in _REQUIRED_COLUMNS if c not in reader.fieldnames]
    if missing:
        raise HTTPException(status_code=400, detail=f"CSV 컬럼 누락: {', '.join(missing)}")

    rows: list[dict] = []
    for r in reader:
        if r is None:
            continue
        gender = r.get("Sex")
        out = dict(r)
        out.pop("Sex", None)
        out["gender"] = gender
        rows.append(out)

    james_upload_info(_SRC, "file=%s rows=%s -> inbound", filename, len(rows))
    result = await use_case.fileupload(
        repository=repository, filename=filename, rows=rows
    )
    return {"count": result["count"], "inserted": result["count"]}

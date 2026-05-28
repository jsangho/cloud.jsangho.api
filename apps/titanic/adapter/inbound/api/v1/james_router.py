from __future__ import annotations

import csv
import io
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import LAYER_LOG
from core.database import get_db
from titanic.app.ports.input.james_use_case import JamesUseCaseImpl, JamesUseCasePort

logger = LAYER_LOG
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

# /titanic/james/fileupload 엔드포인트: Titanic
def get_james_use_case(db: AsyncSession = Depends(get_db)) -> JamesUseCasePort:
    return JamesUseCaseImpl(db=db)


@router.post("/fileupload")
async def upload_titanic_csv(
    file: UploadFile = File(...),
    use_case: JamesUseCasePort = Depends(get_james_use_case),
):
    filename = (file.filename or "").strip() or "<unknown>"
    logger.info("[JamesUpload][%s] file=%s -> inbound(router)", _SRC, filename)
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

    logger.info("[JamesUpload][%s] file=%s -> parsed rows=%s (Sex->gender)", _SRC, filename, len(rows))
    result = await use_case.fileupload(filename=filename, rows=rows)
    logger.info("[JamesUpload][%s] file=%s -> completed inserted=%s", _SRC, filename, result.get("count"))
    return {"count": result.get("count", len(rows)), "inserted": result.get("count", len(rows))}




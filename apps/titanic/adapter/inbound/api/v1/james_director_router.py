from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db, james_director_upload_info
from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorFileuploadResponse,
    JamesDirectorRecordSchema,
    JamesDirectorSchema,
)
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase

logger = logging.getLogger("uvicorn.error")
_SRC = Path(__file__).name

james_director_router = APIRouter(
    prefix="/titanic/james-director", tags=["james-director"]
)

_PREVIEW_FIELDS: tuple[tuple[str, str], ...] = (
    ("passenger_id", "PassengerId"),
    ("survived", "Survived"),
    ("pclass", "Pclass"),
    ("name", "Name"),
    ("gender", "gender"),
    ("age", "Age"),
    ("sib_sp", "SibSp"),
    ("parch", "Parch"),
    ("ticket", "Ticket"),
    ("fare", "Fare"),
    ("cabin", "Cabin"),
    ("embarked", "Embarked"),
)


def _format_preview_record(index: int, record: JamesDirectorRecordSchema) -> str:
    data = record.model_dump()
    label_width = max(len(label) for _, label in _PREVIEW_FIELDS)
    lines = [f"── row {index} " + "─" * 40]
    for field, label in _PREVIEW_FIELDS:
        value = data.get(field, "")
        lines.append(f"  {label:<{label_width}} : {value}")
    return "\n".join(lines)


def get_james_director_use_case(
    db: AsyncSession = Depends(get_db),
) -> JamesDirectorUseCase:
    from titanic.adapter.outbound.pg.james_director_pg_repository import (
        JamesDirectorPgRepository,
    )
    from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor

    return JamesDirectorInteractor(JamesDirectorPgRepository(db))


@james_director_router.post(
    "/fileupload", response_model=JamesDirectorFileuploadResponse
)
async def upload_titanic_csv(
    file: UploadFile = File(...),
    use_case: JamesDirectorUseCase = Depends(get_james_director_use_case),
):
    filename = (file.filename or "").strip() or "<unknown>"
    if not (file.filename or "").lower().endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="CSV 파일(.csv)만 업로드할 수 있습니다."
        )

    raw = await file.read()
    payload = JamesDirectorSchema.from_csv_bytes(raw)
    rows = payload.to_upload_rows()

    # 레코드 목록 상위 5줄만 출력하는 코드 (실제 서비스에서는 제거)
    logger.info("[JamesDirector] 업로드 CSV 파싱 미리보기 (상위 %s건)", min(5, len(payload.records)))
    preview_blocks = [
        _format_preview_record(index, record)
        for index, record in enumerate(payload.records[:5], start=1)
    ]
    logger.info("\n%s", "\n".join(preview_blocks))

    james_director_upload_info(
        _SRC, "file=%s rows=%s -> inbound", filename, len(payload.records)
    )
    result = await use_case.fileupload(filename=filename, rows=rows)
    return JamesDirectorFileuploadResponse(
        count=result["count"],
        inserted=result["count"],
    )

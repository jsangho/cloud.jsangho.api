from __future__ import annotations

import csv
import logging
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorFileuploadResponse,
    TitanicRecordSchema,
    format_preview_record,
)
from titanic.app.ports.input.james_director_use_case import (
    JamesDirectorUseCase,
    get_james_director_use_case,
)
from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor

logger = logging.getLogger("uvicorn.error")


james_director_router = APIRouter(prefix="/james-director", tags=["james-director"])


@james_director_router.post(
    "/fileupload", response_model=JamesDirectorFileuploadResponse
)
async def upload_titanic_file(
    file: UploadFile = File(...),
    use_case: JamesDirectorUseCase = Depends(get_james_director_use_case),
):
    """타이타닉 승객 데이터 CSV 파일 업로드"""
    filename = (file.filename or "").strip() or "<unknown>"
    if file.content_type not in {"text/csv", "application/vnd.ms-excel", "text/plain"}:
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    raw = await file.read()
    text = raw.decode("utf-8", errors="replace")
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    schema = [
        TitanicRecordSchema.model_validate(_normalize_titanic_row(row))
        for row in reader
        if row
    ]

    # 미리보기 로그 출력
    logger.info(
        "[제임스 라우터] 업로드된 CSV파일에서 스키마로 옮겨진 레코드 미리보기 (상위 %s건, file=%s)",
        min(5, len(schema)),
        filename,
    )
    preview_blocks = [
        format_preview_record(index, record)
        for index, record in enumerate(schema[:5], start=1)
    ]
    if preview_blocks:
        logger.info("\n%s", "\n".join(preview_blocks))

    # use_case : JamesDirectorUseCase = JamesDirectorInteractor()
    # (DB 연결이 없어도 동작하도록 Interactor 기본 저장소는 no-op 처리됨)
    use_case: JamesDirectorUseCase = JamesDirectorInteractor()
    
    result = await use_case.receive_uploaded_records(schema)
    return JamesDirectorFileuploadResponse(
        count=result["count"],
        inserted=result["count"],
    )


def _normalize_titanic_row(row: dict) -> dict:
    normalized: dict[str, object] = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        lower_key = key.lower()
        if lower_key == "sex":
            normalized["gender"] = value
        elif lower_key == "passengerid":
            normalized["passenger_id"] = value
        elif lower_key == "sibsp":
            normalized["sib_sp"] = value
        elif lower_key in {
            "survived",
            "pclass",
            "name",
            "age",
            "parch",
            "ticket",
            "fare",
            "cabin",
            "embarked",
            "gender",
        }:
            normalized[lower_key] = value
        else:
            normalized[key] = value
    return normalized

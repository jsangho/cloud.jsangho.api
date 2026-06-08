from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import (
    JamesDirectorFileuploadResponse,
    JamesDirectorMyselfSchema,
    JamesDirectorSchema,
)
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.dependencies.crew_james_director_provider import get_james_director_use_case
from titanic.app.dtos.crew_james_director_dto import JamesDirectorResponse
'''
 감독: 제임스 카메론 (James Cameron)
 전설적인 흥행작 <타이타닉>을 연출하여
 "내가 세상의 왕이다!"를 외친 제임스 카메론 감독의 라우터
 완벽주의 성향으로 타이타닉의 모든 세트와 디테일을
 고증한 아키텍처의 총괄 디렉터 역할 수행
'''

logger = logging.getLogger("uvicorn.error")

james_director_router = APIRouter(prefix="/james", tags=["james"])


def _parse_uploaded_csv(raw: bytes) -> JamesDirectorSchema:
    if not raw.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")
    schema = JamesDirectorSchema.from_csv_bytes(raw)
    if not schema.records:
        raise HTTPException(status_code=400, detail="CSV에 데이터 행이 없습니다.")
    return schema


def _to_fileupload_response(result: dict[str, int]) -> JamesDirectorFileuploadResponse:
    count = result["count"]
    return JamesDirectorFileuploadResponse(count=count, inserted=count)

@james_director_router.get("/myself")
async def introduce_myself(
    use_case: JamesDirectorUseCase = Depends(get_james_director_use_case),
) -> JamesDirectorResponse:
    schema = JamesDirectorMyselfSchema(
        id=1,
        name="James Cameron",
        memo=(
            '전설적인 흥행작 <타이타닉>을 연출하여 "내가 세상의 왕이다!"를 외친 '
            "제임스 카메론 감독. 완벽주의 성향으로 타이타닉의 모든 세트와 디테일을 "
            "고증한 아키텍처의 총괄 디렉터 역할 수행"
        ),
    )
    logger.info("[JamesDirectorRouter] introduce_myself 진입 | request_data=%s", schema)
    return await use_case.introduce_myself(schema)


@james_director_router.post(
    "/fileupload", response_model=JamesDirectorResponse, summary="타이타닉 승객 데이터 CSV 파일 업로드"
)
async def upload_titanic_file( 
    file: UploadFile = File(...),
    james: JamesDirectorUseCase = Depends(get_james_director_use_case),
):
    """타이타닉 승객 데이터 CSV 파일 업로드"""
    schema = _parse_uploaded_csv(await file.read())
    logger.info(
        "[JamesDirectorRouter] upload_titanic_file 진입 | filename=%s rows=%s",
        file.filename,
        len(schema.records),
    )
    result = await james.upload_titanic_file(schema.records)
    return await _to_fileupload_response(result)

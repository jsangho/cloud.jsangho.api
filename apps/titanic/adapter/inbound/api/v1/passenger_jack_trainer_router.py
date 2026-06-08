import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case

'''
잭 도슨 (Jack Dawson)
생존 예측 모델의 핵심 인터페이스를 담당합니다.
'''
logger = logging.getLogger("uvicorn.error")

jack_trainer_router = APIRouter(prefix="/jack", tags=["jack"])


@jack_trainer_router.get("/myself")
async def introduce_myself(
    use_case: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
) -> JackTrainerResponse:
    schema = JackTrainerSchema(
        id=9,
        name="Jack Dawson",
        memo="자유로운 영혼의 3등석 화가. 로즈에게 진정한 삶을 가르쳐준 인물이자 타이타닉 생존 스토리의 주역",
    )
    logger.info("[JackTrainerRouter] introduce_myself 진입 | request_data=%s", schema)
    return await use_case.introduce_myself(schema)

import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema
from titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleResponse
from titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from titanic.dependencies.passenger_isidor_couple_provider import get_isidor_couple_use_case

'''
이시도르 & 이다 스트라우스 부부 (Isidor & Ida Straus)
커플 생존 데이터 담당자
'''
logger = logging.getLogger("uvicorn.error")

isidor_couple_router = APIRouter(prefix="/isidor", tags=["isidor"])


@isidor_couple_router.get("/myself")
async def introduce_myself(
    use_case: IsidorCoupleUseCase = Depends(get_isidor_couple_use_case),
) -> IsidorCoupleResponse:
    schema = IsidorCoupleSchema(
        id=8,
        name="Isidor & Ida Straus",
        memo=(
            '구명보트 탑승을 거부하고 "우리는 평생을 함께했으니 함께 갈 것입니다"라며 '
            "침대 위에서 서로를 꼭 껴안고 물이 차오르는 것을 맞이한 노부부입니다."
        ),
    )
    logger.info("[IsidorCoupleRouter] introduce_myself 진입 | request_data=%s", schema)
    return await use_case.introduce_myself(schema)

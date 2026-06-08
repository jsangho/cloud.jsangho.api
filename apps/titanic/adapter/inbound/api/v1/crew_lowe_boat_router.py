import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.dependencies.crew_lowe_boat_provider import get_lowe_boat_use_case

'''
해롤드 로우 (Harold Lowe)
구명보트 조종을 담당하는 항해사.
'''
logger = logging.getLogger("uvicorn.error")

lowe_boat_router = APIRouter(prefix="/lowe", tags=["lowe"])


@lowe_boat_router.get("/myself")
async def introduce_myself(
    use_case: LoweBoatUseCase = Depends(get_lowe_boat_use_case),
) -> LoweBoatResponse:
    schema = LoweBoatSchema(
        id=4,
        name="Harold Lowe",
        memo="구명보트 조종을 담당하는 항해사.",
    )
    logger.info("[LoweBoatRouter] introduce_myself 진입 | request_data=%s", schema)
    return await use_case.introduce_myself(schema)

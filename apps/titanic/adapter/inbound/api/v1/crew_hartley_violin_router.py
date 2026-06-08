import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.dependencies.crew_hartley_violin_provider import get_hartley_violin_use_case

'''
왈리스 하틀리 (Wallace Hartley - 악단장)
배가 가라앉는 극도의 공포 속에서도 승객들을 진정시키기 위해 끝까지 찬송가를 연주했던 악단장입니다.
'''
logger = logging.getLogger("uvicorn.error")

hartley_violin_router = APIRouter(prefix="/hartley", tags=["hartley"])


@hartley_violin_router.get("/myself")
async def introduce_myself(
    use_case: HartleyViolinUseCase = Depends(get_hartley_violin_use_case),
) -> HartleyViolinResponse:
    schema = HartleyViolinSchema(
        id=3,
        name="Wallace Hartley",
        memo="배가 가라앉는 극도의 공포 속에서도 승객들을 진정시키기 위해 끝까지 찬송가를 연주했던 악단장입니다.",
    )
    logger.info("[HartleyViolinRouter] introduce_myself 진입 | request_data=%s", schema)
    return await use_case.introduce_myself(schema)

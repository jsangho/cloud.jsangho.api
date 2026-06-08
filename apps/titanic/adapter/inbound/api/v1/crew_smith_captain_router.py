import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
'''
logger = logging.getLogger("uvicorn.error")

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.get("/myself")
async def introduce_myself(
    use_case: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithCaptainResponse:
    schema = SmithCaptainSchema(
        id=5,
        name="Captain Edward John Smith",
        memo="타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.",
    )
    logger.info("[SmithCaptainRouter] introduce_myself 진입 | request_data=%s", schema)
    return await use_case.introduce_myself(schema)

from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.responses import StreamingResponse

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatMessageSchema,
    ChatSchema,
    SmithCaptainChatResponseSchema,
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainQuery,
    SmithCaptainResponse,
)
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer
from titanic.dependencies.passenger_rose_model_provider import get_rose_model

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
'''
smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.post("/chat")
async def chat(
    schema: Annotated[ChatSchema, Body()],
    smith: SmithCaptainUseCase = Depends(get_smith_captain),
    jack: JackTrainerUseCase = Depends(get_jack_trainer),
    rose: RoseModelUseCase = Depends(get_rose_model)
):

    response = await smith.chat(schema, jack, rose)
    return SmithCaptainChatResponseSchema(reply=response.reply)


def _format_messages_log(messages: list[ChatMessageSchema]) -> str:
    lines = [
        f"  messages[{index}]: role={message.role} text={message.text!r}"
        for index, message in enumerate(messages)
    ]
    return "\n".join(lines) if lines else "  messages: (비어 있음)"


@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain),
) -> SmithCaptainResponse:
    schema = SmithCaptainSchema(
        id=5,
        name="Captain Edward John Smith",
    )
    query = SmithCaptainQuery(id=schema.id, name=schema.name)
    return await smith.introduce_myself(query)

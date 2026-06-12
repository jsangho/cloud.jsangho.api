import logging
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
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain

logger = logging.getLogger("uvicorn.error")

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
'''
smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.post("/chat")
async def chat(
    schema: Annotated[ChatSchema, Body()],
    smith: SmithCaptainUseCase = Depends(get_smith_captain),
):
    logger.info(
        "[SmithCaptainRouter] POST /api/titanic/smith/chat | stream=%s\n%s",
        schema.stream,
        _format_messages_log(schema.messages),
    )

    if schema.stream:
        return StreamingResponse(
            smith.chat_stream(schema),
            media_type="text/plain; charset=utf-8",
        )

    response = await smith.chat(schema)
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
    logger.info(
        "[SmithCaptainRouter] introduce_myself 진입 | request_data=%s",
        f"id={schema.id} name={schema.name!r}",
    )
    query = SmithCaptainQuery(id=schema.id, name=schema.name)
    return await smith.introduce_myself(query)

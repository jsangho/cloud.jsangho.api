from __future__ import annotations
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse
from titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository

logger = logging.getLogger("uvicorn.error")

class MollyScalerPgRepository(MollyScalerRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        logger.info("[MollyScalerPgRepository] introduce_myself 진입 | request_data=%s", schema)
        return MollyScalerResponse(
            id=schema.id * 10000,
            name=f"{schema.name}가 레포지토리에 다녀옴",
        )
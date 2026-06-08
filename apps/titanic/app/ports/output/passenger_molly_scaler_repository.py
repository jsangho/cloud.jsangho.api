from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse


class MollyScalerRepository(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        '''몰리의 자기소개 메소드'''
        pass
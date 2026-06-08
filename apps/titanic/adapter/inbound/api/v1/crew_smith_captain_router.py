from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.get("/captain")
async def get_smith_captain(
    use_case: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
):
    return await use_case.get_captain()

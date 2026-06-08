from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.dependencies.crew_hartley_violin_provider import get_hartley_violin_use_case

hartley_violin_router = APIRouter(prefix="/hartley", tags=["hartley"])


@hartley_violin_router.get("/violin")
async def get_hartley_violin(
    use_case: HartleyViolinUseCase = Depends(get_hartley_violin_use_case),
):
    return await use_case.get_violin()

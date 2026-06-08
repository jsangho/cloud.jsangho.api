from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.dependencies.crew_andrews_architect_provider import get_andrews_architect_use_case

andrews_architect_router = APIRouter(prefix="/andrews", tags=["andrews"])


@andrews_architect_router.get("/architect")
async def get_andrews_architect(
    use_case: AndrewsArchitectUseCase = Depends(get_andrews_architect_use_case),
):
    return await use_case.get_architect()

from __future__ import annotations

from fastapi import APIRouter, Depends

from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case

cal_tester_router = APIRouter(prefix="/cal", tags=["cal"])


@cal_tester_router.get("/tester")
async def get_cal_tester(
    use_case: CalTesterUseCase = Depends(get_cal_tester_use_case),
):
    return await use_case.get_tester()

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.app.ports.input.titanic_query_port import TitanicQueryPort
from titanic.app.use_cases.titanic_query_impl import TitanicQueryImpl

router = APIRouter(prefix="/titanic/v1", tags=["titanic"])


def get_titanic_query(db: AsyncSession = Depends(get_db)) -> TitanicQueryPort:
    return TitanicQueryImpl(db)


def get_titanic_query_without_db() -> TitanicQueryPort:
    return TitanicQueryImpl(None)


@router.get("/data")
async def read_titanic_data(
    query: TitanicQueryPort = Depends(get_titanic_query),
):
    return await query.get_data()


@router.get("/count")
async def read_titanic_count(
    query: TitanicQueryPort = Depends(get_titanic_query),
):
    count = await query.get_count()
    return {"count": count}


@router.get("/problem")
def read_titanic_problem(
    query: TitanicQueryPort = Depends(get_titanic_query_without_db),
):
    return {"summary": query.get_problem_summary()}


@router.get("/tree")
def read_titanic_tree(
    query: TitanicQueryPort = Depends(get_titanic_query_without_db),
):
    return {"tree": query.has_decision_tree_model()}


@router.get("/model")
def read_titanic_model(
    query: TitanicQueryPort = Depends(get_titanic_query_without_db),
):
    model_name = query.get_model_name()
    return JSONResponse(content=jsonable_encoder(model_name))

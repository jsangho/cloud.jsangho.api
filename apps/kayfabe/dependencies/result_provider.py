from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.result_pg_repository import ResultPgRepository
from kayfabe.app.ports.input.result import ResultUseCase
from kayfabe.app.ports.output.result_repository import ResultRepository
from kayfabe.app.use_cases.result_interactor import ResultInteractor


def get_result(
    db: AsyncSession = Depends(get_db),
) -> ResultUseCase:
    repository: ResultRepository = ResultPgRepository(db)
    return ResultInteractor(repository=repository)

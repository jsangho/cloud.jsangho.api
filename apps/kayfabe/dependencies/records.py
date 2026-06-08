from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.records_pg_repository import RecordsPgRepository
from kayfabe.app.ports.input.records_use_case import RecordsUseCase
from kayfabe.app.ports.output.records_repository import RecordsRepository
from kayfabe.app.use_cases.records_interactor import RecordsInteractor


def get_records_use_case(
    db: AsyncSession = Depends(get_db),
) -> RecordsUseCase:
    records_repository: RecordsRepository = RecordsPgRepository(db)
    return RecordsInteractor(records_repository=records_repository)

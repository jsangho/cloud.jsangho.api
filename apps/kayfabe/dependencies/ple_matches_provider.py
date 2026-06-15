from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.ple_matches_pg_repository import RecordsMyselfPgRepository, RecordsPgRepository
from kayfabe.app.dtos.myself_dto import MyselfRepository, MyselfUseCase
from kayfabe.app.ports.input.ple_matches_use_case import RecordsUseCase
from kayfabe.app.ports.output.ple_matches_repository import RecordsRepository
from kayfabe.app.use_cases.ple_matches_interactor import RecordsInteractor, RecordsMyselfInteractor


def get_records_repository(
    db: AsyncSession = Depends(get_db),
) -> RecordsRepository:
    return RecordsPgRepository(db)


def get_records(
    records_repository: RecordsRepository = Depends(get_records_repository),
) -> RecordsUseCase:
    return RecordsInteractor(records_repository=records_repository)


def get_records_myself_repository(
    db: AsyncSession = Depends(get_db),
) -> MyselfRepository:
    return RecordsMyselfPgRepository(session=db)


def get_records_myself(
    repository: MyselfRepository = Depends(get_records_myself_repository),
) -> MyselfUseCase:
    return RecordsMyselfInteractor(repository=repository)

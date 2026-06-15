from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.ple_events_pg_repository import PlePgRepository
from kayfabe.adapter.outbound.pg.ple_match_pick_pg_repository import (
    RankingMyselfPgRepository,
    RankingPgRepository,
)
from kayfabe.app.dtos.myself_dto import MyselfRepository, MyselfUseCase
from kayfabe.app.ports.input.ple_match_pick_use_case import RankingUseCase
from kayfabe.app.ports.output.ple_events_repository import PleRepository
from kayfabe.app.ports.output.ple_match_pick_repository import RankingRepository
from kayfabe.app.use_cases.ple_match_pick_interactor import RankingInteractor, RankingMyselfInteractor


def get_ranking_repository(
    db: AsyncSession = Depends(get_db),
) -> RankingRepository:
    return RankingPgRepository(db)


def get_ranking_ple_repository(
    db: AsyncSession = Depends(get_db),
) -> PleRepository:
    return PlePgRepository(db)


def get_ranking(
    ranking_repository: RankingRepository = Depends(get_ranking_repository),
    ple_repository: PleRepository = Depends(get_ranking_ple_repository),
) -> RankingUseCase:
    return RankingInteractor(
        ranking_repository=ranking_repository,
        ple_repository=ple_repository,
    )


def get_ranking_myself_repository(db: AsyncSession = Depends(get_db)) -> MyselfRepository:
    return RankingMyselfPgRepository(session=db)


def get_ranking_myself(
    repository: MyselfRepository = Depends(get_ranking_myself_repository),
) -> MyselfUseCase:
    return RankingMyselfInteractor(repository=repository)

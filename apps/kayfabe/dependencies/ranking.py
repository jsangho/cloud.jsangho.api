from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from kayfabe.adapter.outbound.pg.ple_pg_repository import PlePgRepository
from kayfabe.adapter.outbound.pg.ranking_pg_repository import RankingPgRepository
from kayfabe.app.ports.input.ranking_use_case import RankingUseCase
from kayfabe.app.ports.output.ple_repository import PleRepository
from kayfabe.app.ports.output.ranking_repository import RankingRepository
from kayfabe.app.use_cases.ranking_interactor import RankingInteractor


def get_ranking_use_case(
    db: AsyncSession = Depends(get_db),
) -> RankingUseCase:
    ranking_repository: RankingRepository = RankingPgRepository(db)
    ple_repository: PleRepository = PlePgRepository(db)
    return RankingInteractor(
        ranking_repository=ranking_repository,
        ple_repository=ple_repository,
    )

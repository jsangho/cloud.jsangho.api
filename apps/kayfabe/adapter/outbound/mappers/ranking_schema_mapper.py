from kayfabe.adapter.inbound.api.schemas.ranking_schema import RankingRowSchema, RankingsResponseSchema
from kayfabe.app.dtos.ranking_dto import RankingsDto


def rankings_to_schema(dto: RankingsDto) -> RankingsResponseSchema:
    return RankingsResponseSchema(
        rows=[
            RankingRowSchema(
                rank=r.rank,
                nickname=r.nickname,
                score=r.score,
                accuracy=r.accuracy,
            )
            for r in dto.rows
        ],
        my_rank=(
            RankingRowSchema(
                rank=dto.my_rank.rank,
                nickname=dto.my_rank.nickname,
                score=dto.my_rank.score,
                accuracy=dto.my_rank.accuracy,
            )
            if dto.my_rank
            else None
        ),
    )

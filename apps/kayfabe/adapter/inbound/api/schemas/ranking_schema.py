from pydantic import BaseModel, ConfigDict, Field


class RankingRowSchema(BaseModel):
    rank: int
    nickname: str
    score: int
    accuracy: float = Field(..., ge=0.0, le=1.0, description="적중률 0~1")

    model_config = ConfigDict(populate_by_name=True)


class RankingsResponseSchema(BaseModel):
    rows: list[RankingRowSchema]
    my_rank: RankingRowSchema | None = Field(default=None, alias="myRank")

    model_config = ConfigDict(populate_by_name=True)


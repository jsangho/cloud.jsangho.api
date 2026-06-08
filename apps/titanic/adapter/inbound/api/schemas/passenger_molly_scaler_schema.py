"""{stem} API 스키마."""

from pydantic import BaseModel


class MollyScalerSchema(BaseModel):
    id: int = 1
    name: str = "Molly Brown"
    memo: str = "특성 스케일링 검증"

from __future__ import annotations

import csv
import io

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, ValidationError

JAMES_DIRECTOR_REQUIRED_COLUMNS = (
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
)


class JamesDirectorRecordSchema(BaseModel):
    """CSV 1행. `Sex` 컬럼은 `gender` 필드로 매핑합니다."""

    model_config = ConfigDict(populate_by_name=True)

    passenger_id: str = Field(alias="PassengerId")
    survived: str = Field(alias="Survived")
    pclass: str = Field(alias="Pclass")
    name: str = Field(alias="Name")
    gender: str | None = Field(default=None, alias="Sex")
    age: str = Field(alias="Age")
    sib_sp: str = Field(alias="SibSp")
    parch: str = Field(alias="Parch")
    ticket: str = Field(alias="Ticket")
    fare: str = Field(alias="Fare")
    cabin: str = Field(alias="Cabin")
    embarked: str = Field(alias="Embarked")

    def to_upload_row(self) -> dict[str, str | None]:
        return {
            "PassengerId": self.passenger_id,
            "Survived": self.survived,
            "Pclass": self.pclass,
            "Name": self.name,
            "gender": self.gender,
            "Age": self.age,
            "SibSp": self.sib_sp,
            "Parch": self.parch,
            "Ticket": self.ticket,
            "Fare": self.fare,
            "Cabin": self.cabin,
            "Embarked": self.embarked,
        }


class JamesDirectorSchema(BaseModel):
    """CSV 업로드 본문을 `JamesDirectorRecordSchema` 목록으로 담는 스키마."""

    records: list[JamesDirectorRecordSchema] = Field(default_factory=list)

    @staticmethod
    def _decode_csv_bytes(raw: bytes) -> str:
        for enc in ("utf-8-sig", "utf-8", "cp949"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        raise HTTPException(
            status_code=400,
            detail="CSV 인코딩을 해석할 수 없습니다. UTF-8로 저장해 주세요.",
        )

    @classmethod
    def from_csv_bytes(cls, raw: bytes) -> JamesDirectorSchema:
        return cls.from_csv_text(cls._decode_csv_bytes(raw))

    @classmethod
    def from_csv_text(cls, text: str) -> JamesDirectorSchema:
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

        missing = [
            c for c in JAMES_DIRECTOR_REQUIRED_COLUMNS if c not in reader.fieldnames
        ]
        if missing:
            raise HTTPException(
                status_code=400, detail=f"CSV 컬럼 누락: {', '.join(missing)}"
            )

        records: list[JamesDirectorRecordSchema] = []
        for row in reader:
            if row is None:
                continue
            try:
                records.append(JamesDirectorRecordSchema.model_validate(row))
            except ValidationError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"CSV 행 형식이 올바르지 않습니다: {exc.errors()}",
                ) from exc

        return cls(records=records)

    def to_upload_rows(self) -> list[dict[str, str | None]]:
        return [record.to_upload_row() for record in self.records]


class JamesDirectorFileuploadResponse(BaseModel):
    count: int
    inserted: int

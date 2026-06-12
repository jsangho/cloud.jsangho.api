from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Gender:
    value: GenderType

    _NORMALIZE_MAP: ClassVar[dict[str, GenderType]] = {
        "male": GenderType.MALE,
        "m": GenderType.MALE,
        "female": GenderType.FEMALE,
        "f": GenderType.FEMALE,
    }

    @classmethod
    def from_raw(cls, raw: str | None) -> Gender:
        if raw is None:
            return cls(value=GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        return cls(value=cls._NORMALIZE_MAP.get(normalized, GenderType.UNKNOWN))

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    def __str__(self) -> str:
        return self.value.value


@dataclass(frozen=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("PassengerId는 빈 값일 수 없습니다.")
        object.__setattr__(self, "value", stripped)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PassengerName:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("PassengerName은 빈 값일 수 없습니다.")
        if len(self.value) > 200:
            raise ValueError(f"PassengerName은 200자를 초과할 수 없습니다: '{self.value}'")

    @property
    def full_name(self) -> str:
        return self.value

    @property
    def normalized(self) -> str:
        return self.value.strip()

    def __str__(self) -> str:
        return self.value


_MAX_AGE = 120.0


@dataclass(frozen=True)
class Age:
    value: float | None

    def __post_init__(self) -> None:
        if self.value is None:
            return
        if self.value < 0:
            raise ValueError(f"Age는 0 이상이어야 합니다: {self.value}")
        if self.value > _MAX_AGE:
            raise ValueError(f"Age는 {_MAX_AGE} 이하이어야 합니다: {self.value}")

    @classmethod
    def from_raw(cls, raw: str | None) -> Age:
        if raw is None or not raw.strip():
            return cls(value=None)
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise ValueError(f"Age 파싱 실패: '{raw}'")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        return self.value is not None and self.value < 18.0

    def __str__(self) -> str:
        return "" if self.value is None else str(self.value)


@dataclass(frozen=True)
class FamilyRelation:
    sib_sp: int
    parch: int

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError(f"sib_sp는 0 이상이어야 합니다: {self.sib_sp}")
        if self.parch < 0:
            raise ValueError(f"parch는 0 이상이어야 합니다: {self.parch}")

    @classmethod
    def from_raw(cls, sib_sp_raw: str | None, parch_raw: str | None) -> FamilyRelation:
        try:
            sib_sp = int(sib_sp_raw.strip()) if sib_sp_raw else 0
        except ValueError:
            raise ValueError(f"sib_sp 파싱 실패: '{sib_sp_raw}'")
        try:
            parch = int(parch_raw.strip()) if parch_raw else 0
        except ValueError:
            raise ValueError(f"parch 파싱 실패: '{parch_raw}'")
        return cls(sib_sp=sib_sp, parch=parch)

    @property
    def total_family_size(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_size == 0


@dataclass(frozen=True)
class SurvivalStatus:
    survived: bool | None = None

    @classmethod
    def from_raw(cls, raw: str | None) -> SurvivalStatus:
        if raw is None or not raw.strip():
            return cls(survived=None)
        stripped = raw.strip()
        if stripped == "1":
            return cls(survived=True)
        if stripped == "0":
            return cls(survived=False)
        raise ValueError(f"SurvivalStatus 파싱 실패: '{raw}'")

    @property
    def is_unknown(self) -> bool:
        return self.survived is None

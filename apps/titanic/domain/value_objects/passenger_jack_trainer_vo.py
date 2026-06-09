from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# ============================================================
# Gender
# ============================================================

class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass(frozen=True)
class Gender:
    value: GenderType

    _NORMALIZE_MAP: dict[str, GenderType] = {
        "male": GenderType.MALE,
        "m": GenderType.MALE,
        "female": GenderType.FEMALE,
        "f": GenderType.FEMALE,
    }

    @classmethod
    def from_str(cls, raw: str) -> Gender:
        normalized = raw.strip().lower()
        gender_type = cls._NORMALIZE_MAP.get(normalized)
        if gender_type is None:
            raise ValueError(
                f"유효하지 않은 Gender 값입니다: '{raw}'. "
                f"허용 값: {set(cls._NORMALIZE_MAP.keys())}"
            )
        return cls(value=gender_type)

    @property
    def is_male(self) -> bool:
        return self.value == GenderType.MALE

    @property
    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    def __str__(self) -> str:
        return self.value.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Gender):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


# ============================================================
# PassengerId
# ============================================================

@dataclass(frozen=True)
class PassengerId:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("PassengerId는 빈 값일 수 없습니다.")
        if not stripped.isdigit():
            raise ValueError(f"PassengerId는 숫자 형식이어야 합니다: '{stripped}'")
        object.__setattr__(self, "value", stripped)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


# ============================================================
# PassengerName
# ============================================================

@dataclass(frozen=True)
class PassengerName:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip() if self.value else ""
        if not stripped:
            raise ValueError("PassengerName은 빈 값일 수 없습니다.")
        if len(stripped) > 100:
            raise ValueError(f"PassengerName은 100자를 초과할 수 없습니다: '{stripped}'")
        object.__setattr__(self, "value", stripped)

    @property
    def last_name(self) -> str:
        """'Braund, Mr. Owen Harris' 형식에서 성(Last name) 추출"""
        return self.value.split(",")[0].strip()

    @property
    def title(self) -> str | None:
        """'Mr.', 'Mrs.', 'Miss.' 등 호칭 추출"""
        if "," not in self.value:
            return None
        rest = self.value.split(",", 1)[1].strip()
        parts = rest.split(".")
        return (parts[0].strip() + ".") if len(parts) >= 2 else None

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerName):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


# ============================================================
# Age
# ============================================================

_MIN_AGE = 0.0
_MAX_AGE = 150.0


@dataclass(frozen=True)
class Age:
    value: float

    def __post_init__(self) -> None:
        if self.value < _MIN_AGE:
            raise ValueError(f"Age는 0 이상이어야 합니다: {self.value}")
        if self.value > _MAX_AGE:
            raise ValueError(f"Age는 {_MAX_AGE} 이하이어야 합니다: {self.value}")

    @classmethod
    def from_str(cls, raw: str) -> Age:
        try:
            return cls(value=float(raw.strip()))
        except ValueError:
            raise ValueError(f"Age는 숫자 형식이어야 합니다: '{raw}'")

    @property
    def is_child(self) -> bool:
        return self.value < 18.0

    @property
    def is_adult(self) -> bool:
        return 18.0 <= self.value < 65.0

    @property
    def is_senior(self) -> bool:
        return self.value >= 65.0

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Age):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


# ============================================================
# FamilyInfo  (SibSp + Parch 묶음 — 항상 함께 의미를 가짐)
# ============================================================

@dataclass(frozen=True)
class FamilyInfo:
    sib_sp: int   # 함께 탑승한 형제/배우자 수
    parch: int    # 함께 탑승한 부모/자녀 수

    def __post_init__(self) -> None:
        for field_name, val in (("sib_sp", self.sib_sp), ("parch", self.parch)):
            if val < 0:
                raise ValueError(f"{field_name}는 0 이상이어야 합니다: {val}")
            if val > 20:
                raise ValueError(f"{field_name}가 비현실적인 값입니다: {val}")

    @classmethod
    def from_str(cls, sib_sp_raw: str, parch_raw: str) -> FamilyInfo:
        try:
            sib_sp = int(sib_sp_raw.strip())
        except ValueError:
            raise ValueError(f"SibSp는 정수 형식이어야 합니다: '{sib_sp_raw}'")
        try:
            parch = int(parch_raw.strip())
        except ValueError:
            raise ValueError(f"Parch는 정수 형식이어야 합니다: '{parch_raw}'")
        return cls(sib_sp=sib_sp, parch=parch)

    @property
    def total_family_members(self) -> int:
        """본인 제외 동승 가족 수"""
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_members == 0

    @property
    def is_large_family(self) -> bool:
        """4인 이상 대가족"""
        return self.total_family_members >= 4

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FamilyInfo):
            return False
        return self.sib_sp == other.sib_sp and self.parch == other.parch

    def __hash__(self) -> int:
        return hash((self.sib_sp, self.parch))


# ============================================================
# SurvivalStatus
# ============================================================

class SurvivalResult(int, Enum):
    NOT_SURVIVED = 0
    SURVIVED = 1


@dataclass(frozen=True)
class SurvivalStatus:
    value: SurvivalResult

    @classmethod
    def from_str(cls, raw: str) -> SurvivalStatus:
        stripped = raw.strip()
        if stripped == "1":
            return cls(value=SurvivalResult.SURVIVED)
        if stripped == "0":
            return cls(value=SurvivalResult.NOT_SURVIVED)
        raise ValueError(
            f"유효하지 않은 SurvivalStatus 값입니다: '{raw}'. 허용 값: '0', '1'"
        )

    @property
    def is_survived(self) -> bool:
        return self.value == SurvivalResult.SURVIVED

    def __str__(self) -> str:
        return str(self.value.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SurvivalStatus):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
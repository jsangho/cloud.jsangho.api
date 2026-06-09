from __future__ import annotations

from dataclasses import dataclass, field

from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyInfo,
    Gender,
    PassengerId,
    PassengerName,
    SurvivalResult,
    SurvivalStatus,
)


@dataclass
class Passenger:
    """
    Passenger Entity
    ─────────────────────────────────────────────────────────
    [DDD 원칙]
    - 동등성(Equality): DB PK(id) 기준으로 판단합니다.
      VO 처럼 값 전체가 아니라 식별자만으로 같은 객체임을 보장합니다.
    - 불변 속성: 각 필드는 VO로 래핑되어 내부 규칙을 스스로 보호합니다.
    - 비즈니스 규칙: record_survival() 처럼 도메인 메서드로 캡슐화합니다.
    - 상태 변경: 외부에서 필드를 직접 교체하지 않고 도메인 메서드를 통해서만 변경합니다.
    - Factory: create() 클래스메서드를 통해 원시값 → VO 변환을 한 곳에서 처리합니다.
    """

    # ------------------------------------------------------------------
    # 식별자 (Surrogate Key)
    # ------------------------------------------------------------------
    id: int  # DB PK — Entity 동등성 기준

    # ------------------------------------------------------------------
    # Value Objects
    # ------------------------------------------------------------------
    passenger_id: PassengerId | None
    name: PassengerName | None
    gender: Gender | None
    age: Age | None
    family_info: FamilyInfo | None  # SibSp + Parch 묶음
    survived: SurvivalStatus | None

    # ------------------------------------------------------------------
    # 도메인 이벤트 버스 (필요 시 ApplicationService 에서 수거)
    # ------------------------------------------------------------------
    _domain_events: list[object] = field(
        default_factory=list, init=False, repr=False, compare=False
    )

    # ==================================================================
    # Factory
    # ==================================================================
    @classmethod
    def create(
        cls,
        *,
        id: int,
        passenger_id: str | None = None,
        name: str | None = None,
        gender: str | None = None,
        age: str | None = None,
        sib_sp: str | None = None,
        parch: str | None = None,
        survived: str | None = None,
    ) -> Passenger:
        """
        ORM / DTO 의 원시 문자열을 받아 VO 로 변환한 뒤 Entity 를 생성합니다.
        유효성 검사는 각 VO 생성자 내부에서 수행됩니다.
        """
        return cls(
            id=id,
            passenger_id=PassengerId(passenger_id) if passenger_id else None,
            name=PassengerName(name) if name else None,
            gender=Gender.from_str(gender) if gender else None,
            age=Age.from_str(age) if age else None,
            family_info=(
                FamilyInfo.from_str(sib_sp, parch)
                if sib_sp is not None and parch is not None
                else None
            ),
            survived=SurvivalStatus.from_str(survived) if survived else None,
        )

    # ==================================================================
    # Domain Methods (비즈니스 규칙 캡슐화)
    # ==================================================================

    def record_survival(self, survived: bool) -> None:
        """
        생존 여부를 최초 1회만 기록할 수 있습니다.
        이미 기록된 경우 도메인 예외를 발생시킵니다.
        """
        if self.survived is not None:
            raise ValueError(
                f"Passenger(id={self.id})의 생존 여부는 이미 기록되어 있습니다."
            )
        self.survived = SurvivalStatus(
            value=SurvivalResult.SURVIVED if survived else SurvivalResult.NOT_SURVIVED
        )

    def correct_age(self, new_age: str) -> None:
        """나이 오기재 정정. 0 미만·150 초과는 VO 레벨에서 차단됩니다."""
        self.age = Age.from_str(new_age)

    # ==================================================================
    # Derived Properties (읽기 전용 비즈니스 질의)
    # ==================================================================

    @property
    def has_survived(self) -> bool:
        return self.survived is not None and self.survived.is_survived

    @property
    def is_traveling_alone(self) -> bool:
        return self.family_info is not None and self.family_info.is_alone

    @property
    def is_child(self) -> bool:
        return self.age is not None and self.age.is_child

    @property
    def is_large_family(self) -> bool:
        return self.family_info is not None and self.family_info.is_large_family

    # ==================================================================
    # Domain Events
    # ==================================================================

    def pull_domain_events(self) -> list[object]:
        """ApplicationService 에서 호출해 이벤트를 수거하고 버퍼를 비웁니다."""
        events, self._domain_events = self._domain_events, []
        return events

    # ==================================================================
    # Identity (Entity 는 식별자로만 동등성 판단)
    # ==================================================================

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Passenger):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"Passenger("
            f"id={self.id}, "
            f"passenger_id={self.passenger_id}, "
            f"name={self.name}, "
            f"gender={self.gender}, "
            f"age={self.age}, "
            f"family_info={self.family_info}, "
            f"survived={self.survived}"
            f")"
        )
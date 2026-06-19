"""piper_hendricks_ceo 슬라이스 Mapper — Entity ↔ HendricksCeoOrm (기획 홀딩)."""

from __future__ import annotations

from silicon_valley.adapter.outbound.orm.piper_hendricks_ceo_orm import HendricksCeoOrm


class HendricksCeoMapper:
    """ORM·Entity 연결. Entity/ORM 테이블 정의 후 to_entity·to_orm 구현."""

    orm_class = HendricksCeoOrm

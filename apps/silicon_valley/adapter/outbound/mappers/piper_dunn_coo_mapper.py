"""piper_dunn_coo 슬라이스 Mapper — Entity ↔ DunnCooOrm (기획 홀딩)."""

from __future__ import annotations

from silicon_valley.adapter.outbound.orm.piper_dunn_coo_orm import DunnCooOrm


class DunnCooMapper:
    """ORM·Entity 연결. Entity/ORM 테이블 정의 후 to_entity·to_orm 구현."""

    orm_class = DunnCooOrm

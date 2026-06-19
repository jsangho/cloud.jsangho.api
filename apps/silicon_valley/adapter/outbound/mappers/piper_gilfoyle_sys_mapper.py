"""piper_gilfoyle_sys 슬라이스 Mapper — Entity ↔ GilfoyleSysOrm (기획 홀딩)."""

from __future__ import annotations

from silicon_valley.adapter.outbound.orm.piper_gilfoyle_sys_orm import GilfoyleSysOrm


class GilfoyleSysMapper:
    """ORM·Entity 연결. Entity/ORM 테이블 정의 후 to_entity·to_orm 구현."""

    orm_class = GilfoyleSysOrm

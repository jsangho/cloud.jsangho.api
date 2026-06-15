from __future__ import annotations

from dataclasses import dataclass

from user.domain.value_objects.role import UserRole


@dataclass(frozen=True)
class JasonMaskSchema:
    login_id: str
    nickname: str
    email: str
    password: str
    password_confirm: str
    role: UserRole

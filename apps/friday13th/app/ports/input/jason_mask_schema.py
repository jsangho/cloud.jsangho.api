from pydantic import BaseModel


class JasonMaskSchema(BaseModel):
    login_id: str
    nickname: str
    email: str
    password: str
    password_confirm: str
    role: str

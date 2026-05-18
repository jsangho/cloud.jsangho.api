from pydantic import BaseModel

class UserSchema(BaseModel):
    nickname: str 
    email: str
    password: str
    password_confirm: str
    role: str

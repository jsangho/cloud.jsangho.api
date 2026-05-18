import logging

from secom.app.schemas.user_schema import UserSchema
from secom.app.repositories.user_repository import UserRepository

logger = logging.getLogger("uvicorn.error")


def _schema_values(user_schema: UserSchema):
    return user_schema.model_dump() if hasattr(user_schema, "model_dump") else user_schema.dict()


class UserService:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        logger.info(
            "\n"
            "========== UserService.save_user ==========\n"
            "현재 레이어: service\n"
            "user_schema=%s\n"
            "========================================",
            _schema_values(user_schema),
        )
        user_repository = UserRepository()
        user_repository.save_user(user_schema)

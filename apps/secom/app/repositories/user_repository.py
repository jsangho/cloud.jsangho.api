import logging

from secom.app.schemas.user_schema import UserSchema
from secom.app.models.user_model import UserModel

logger = logging.getLogger("uvicorn.error")


def _schema_values(user_schema: UserSchema):
    return user_schema.model_dump() if hasattr(user_schema, "model_dump") else user_schema.dict()


class UserRepository:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        logger.info(
            "\n"
            "========== UserRepository.save_user ==========\n"
            "현재 레이어: repository\n"
            "user_schema=%s\n"
            "============================================",
            _schema_values(user_schema),
        )


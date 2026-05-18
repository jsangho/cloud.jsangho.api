import logging

from secom.app.schemas.user_schema import UserSchema
from secom.app.services.user_service import UserService

logger = logging.getLogger("uvicorn.error")


def _schema_values(user_schema: UserSchema):
    return user_schema.model_dump() if hasattr(user_schema, "model_dump") else user_schema.dict()


class UserController:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        logger.info(
            "\n"
            "========== UserController.save_user ==========\n"
            "현재 레이어: controller\n"
            "user_schema=%s\n"
            "============================================",
            _schema_values(user_schema),
        )
        user_service = UserService()
        user_service.save_user(user_schema)

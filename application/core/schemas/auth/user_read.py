from core.types_own.user_id import UserIdType
from fastapi_users import schemas


class UserRead(schemas.BaseUser[UserIdType]):
    pass

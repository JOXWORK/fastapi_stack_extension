from __future__ import annotations

from typing import TYPE_CHECKING, Generic

from fastapi_users import models

if TYPE_CHECKING:

    from .user_database_own import SQLAlchemyUserDatabaseOwn

from fastapi_users import BaseUserManager


class BaseUserManagerOwn(Generic[models.UP, models.ID], BaseUserManager[models.UP, models.ID]):
    def __init__(
        self,
        user_db: SQLAlchemyUserDatabaseOwn,
        password_helper=None,
    ):
        super().__init__(
            user_db=user_db,
            password_helper=password_helper,
        )

        self.user_db: SQLAlchemyUserDatabaseOwn

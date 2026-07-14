from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.models.user import User

from fastapi_users import exceptions
from fastapi_users.db import SQLAlchemyUserDatabase


class SQLAlchemyUserDatabaseOwn(SQLAlchemyUserDatabase):
    def __init__(
        self,
        session: AsyncSession,
        user_table: User,
        oauth_account_table=None,
    ):
        super().__init__(
            session=session,
            user_table=user_table,
            oauth_account_table=oauth_account_table,
        )

    async def check(self, user: User) -> None:
        if not user.is_active:
            raise exceptions.UserInactive()

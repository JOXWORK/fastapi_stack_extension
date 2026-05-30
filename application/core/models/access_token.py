from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    AsyncSession,
    Mapped,
    SQLAlchemyBaseAccessTokenTable,
    String,
    mapped_column,
)
from sqlalchemy import ForeignKey

from core.types_own.user_id import UserIdType

from .base import Base


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIdType]):
    token: Mapped[str] = mapped_column(
        String(length=43),
        primary_key=True,
        unique=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="cascade",
        )
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session=session, user_table=cls)

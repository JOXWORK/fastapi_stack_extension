from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from core.models.mixins import BaseIntIdPkMixin
from core.types_own.user_id import UserIdType

from .base import Base


class User(
    Base,
    SQLAlchemyBaseUserTable[UserIdType],
    BaseIntIdPkMixin,
):
    name: Mapped[str | None] = mapped_column(String(50))

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(
            session=session,
            user_table=cls,
        )

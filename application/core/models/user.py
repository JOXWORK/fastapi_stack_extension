from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import BaseIntIdPkMixin
from core.types_own.user_id import UserIdType


class User(
    Base,
    BaseIntIdPkMixin,
    SQLAlchemyBaseUserTable[UserIdType],
):
    name: Mapped[str | None] = mapped_column(String(50))

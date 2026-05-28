from core.models import Base
from core.types_own.user_id import UserIdType
from fastapi_users_db_sqlalchemy.access_token import (
    Mapped,
    SQLAlchemyBaseAccessTokenTable,
    String,
    mapped_column,
)
from sqlalchemy import ForeignKey


class AccessToken(SQLAlchemyBaseAccessTokenTable[UserIdType], Base):
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

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import BaseIntIdPkMixin


class UserSession(Base, BaseIntIdPkMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="cascade",
        )
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        default=datetime.now(timezone.utc),
    )

    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)

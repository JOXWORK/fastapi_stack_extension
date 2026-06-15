from datetime import datetime, timedelta

from fastapi_users_db_sqlalchemy.generics import now_utc
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.config import settings


def calc_expires_at(
    lifetime_seconds: float = 0,
    lifetime_minutes: float = 0,
    lifetime_hours: float = 0,
    lifetime_days: float = 0,
    lifetime_weeks: float = 0,
):
    now_time = now_utc()
    expires_delta = timedelta(
        seconds=lifetime_seconds,
        minutes=lifetime_minutes,
        hours=lifetime_hours,
        days=lifetime_days,
        weeks=lifetime_weeks,
    )

    return now_time + expires_delta


class UserSessionExpiresAtMixin:
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        default=calc_expires_at(
            lifetime_minutes=settings.auth.user_session.lifetime_minutes,
            lifetime_hours=settings.auth.user_session.lifetime_hours,
            lifetime_days=settings.auth.user_session.lifetime_days,
        ),
    )

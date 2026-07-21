from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.generics import now_utc

if TYPE_CHECKING:
    from core.models import RefreshToken, UserSession

from core.config import settings

from .own.exceptions_own import RefreshTokenNotExists, UserSessionExpires, UserSessionNotExists, UserSessionRevoked


class Validator:
    def __init__(
        self,
        force_raise: bool = False,
        lifetime_seconds: float = 0,
        lifetime_minutes: float = 0,
        lifetime_hours: float = 0,
        lifetime_days: float = 0,
        lifetime_weeks: float = 0,
    ):
        self.force_raise = force_raise
        self.lifetime_seconds = lifetime_seconds
        self.lifetime_minutes = lifetime_minutes
        self.lifetime_hours = lifetime_hours
        self.lifetime_days = lifetime_days
        self.lifetime_weeks = lifetime_weeks

    async def check_user_session(
        self,
        user_session: UserSession,
        force_raise: bool | None = None,
        not_exists_raise: bool = False,
    ) -> list[UserSessionExpires | UserSessionRevoked | UserSessionNotExists]:
        force_raise_ = self.force_raise or force_raise
        errors = []

        if not_exists_raise and user_session is None:
            if force_raise_:
                raise UserSessionNotExists()
            errors.append(UserSessionNotExists)

        if not hasattr(user_session, "expires_at"):
            user_session_expires_at = user_session.created_at + timedelta(
                seconds=self.lifetime_seconds,
                minutes=self.lifetime_minutes,
                hours=self.lifetime_hours,
                days=self.lifetime_days,
                weeks=self.lifetime_weeks,
            )
        else:
            user_session_expires_at = user_session.expires_at

        if now_utc() > user_session_expires_at:
            if force_raise_:
                raise UserSessionExpires()
            errors.append(UserSessionExpires)

        if user_session.revoked_at:
            if force_raise_:
                raise UserSessionRevoked()
            errors.append(UserSessionRevoked)

        return errors

    # async def check_refresh_token(self, refresh_token: RefreshToken)


validator = Validator(
    force_raise=False,
    lifetime_minutes=settings.auth.user_session.lifetime_minutes,
    lifetime_hours=settings.auth.user_session.lifetime_hours,
    lifetime_days=settings.auth.user_session.lifetime_days,
)

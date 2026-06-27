from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.models import AccessToken, User


from core.models.user_session import UserSession

from .exceptions_own import UserSessionInvalid


class UserSessionDatabase:
    def __init__(
        self,
        session: AsyncSession,
        lifetime_seconds: float = 0,
        lifetime_minutes: float = 0,
        lifetime_hours: float = 0,
        lifetime_days: float = 0,
        lifetime_weeks: float = 0,
    ):
        self.session = session
        self.lifetime_seconds = lifetime_seconds
        self.lifetime_minutes = lifetime_minutes
        self.lifetime_hours = lifetime_hours
        self.lifetime_days = lifetime_days
        self.lifetime_weeks = lifetime_weeks

    async def check_user_session(self, access_token: AccessToken) -> None:
        user_session = await self.session.get(UserSession, access_token.session_id)

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

        if datetime.now(timezone.utc) > user_session_expires_at or user_session.revoked_at:
            raise UserSessionInvalid

    async def create_user_session(self, user: User) -> UserSession:
        user_session = UserSession(user_id=user.id)
        self.session.add(user_session)
        await self.session.commit()
        await self.session.refresh(user_session)

        return user_session

    async def destroy_session(self, access_token: AccessToken) -> None:
        user_session = await self.session.get(UserSession, access_token.session_id)
        await self.session.delete(user_session)
        await self.session.commit()

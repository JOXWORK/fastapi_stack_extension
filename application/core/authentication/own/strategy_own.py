from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from fastapi_users import BaseUserManager, exceptions
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.password import PasswordHelper

from core.models import User, UserSession

from .exceptions_own import UserSessionInvalid
from .refresh_token_database import RefreshTokenDatabase
from .user_session_database import UserSessionDatabase


class StrategyOwn(DatabaseStrategy):
    def __init__(
        self,
        user_session_database: UserSessionDatabase,
        database: AccessTokenDatabase,
        refresh_token_database: RefreshTokenDatabase,
        lifetime_seconds=None,
    ):
        self.user_session_database = user_session_database
        self.refresh_token_database = refresh_token_database
        self.password_helper = PasswordHelper()
        super().__init__(database, lifetime_seconds)

    async def read_token(
        self,
        token: str | None,
        user_manager: BaseUserManager,
    ) -> User | None:
        if token is None:
            return None

        max_age = None
        if self.lifetime_seconds:
            max_age = datetime.now(timezone.utc) - timedelta(seconds=self.lifetime_seconds)

        access_token = await self.database.get_by_token(token, max_age)
        if access_token is None:
            return None

        try:
            await self.user_session_database.check_user_session(access_token=access_token)
            parsed_id = user_manager.parse_id(access_token.user_id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID, UserSessionInvalid):
            return None

    async def write_token(self, user: User) -> tuple[str, str]:
        user_session = await self.user_session_database.create_user_session(user=user)

        access_token_dict = self._create_access_token_dict(user)
        access_token_dict.update({"session_id": user_session.id})

        refresh_token_dict = await self._create_refresh_token_dict(
            user_session=user_session,
            user=user,
        )
        refresh_token_unhashed = refresh_token_dict.pop("refresh_token")

        access_token = await self.database.create(access_token_dict)
        refresh_token = await self.refresh_token_database.create_refresh_token(refresh_token_dict=refresh_token_dict)  # noqa: F841

        return access_token.token, refresh_token_unhashed

    async def destroy_token(self, token: str, user: User, *, session_destroy: bool = True) -> None:
        access_token = await self.database.get_by_token(token)
        if access_token is not None:
            if session_destroy:
                await self.user_session_database.destroy_session(access_token=access_token)
            else:
                await self.database.delete(access_token)

    async def _create_refresh_token_dict(
        self,
        user_session: UserSession,
        user: User,
    ) -> dict[str, str, int, int]:
        refresh_token = token_urlsafe()
        token_hash = self.password_helper.hash(refresh_token)

        return {
            "refresh_token": refresh_token,
            "token_hash": token_hash,
            "session_id": user_session.id,
            "user_id": user.id,
        }

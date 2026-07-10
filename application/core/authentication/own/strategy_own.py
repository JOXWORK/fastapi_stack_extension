from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import TYPE_CHECKING

from fastapi_users import exceptions
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from core.config import settings

from .exceptions_own import UserSessionInvalid

if TYPE_CHECKING:
    from fastapi_users import BaseUserManager

    from core.models import AccessToken, User

    from .access_token_own import SQLAlchemyAccessTokenDatabaseOwn
    from .refresh_token_database import RefreshTokenDatabase
    from .user_session_database import UserSessionDatabase


class StrategyOwn(DatabaseStrategy):
    def __init__(
        self,
        user_session_database: UserSessionDatabase,
        database: SQLAlchemyAccessTokenDatabaseOwn,
        refresh_token_database: RefreshTokenDatabase,
        lifetime_seconds=None,
    ):
        self.user_session_database = user_session_database
        self.refresh_token_database = refresh_token_database
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

        user_session = await self.user_session_database.get(access_token.session_id)
        if user_session is None:
            return None

        try:
            await self.user_session_database.check(user_session)
            parsed_id = user_manager.parse_id(access_token.user_id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID, UserSessionInvalid):
            return None

    async def read_token_ignore_expire(self, token: str | None) -> AccessToken:
        if token is None:
            return None

        access_token = await self.database.get_token_ignore_expire(token=token)

        if access_token is None:
            return None

        return access_token

    async def write_token(self, user: User) -> tuple[str, str]:
        user_session = await self.user_session_database.create(user=user)

        access_token_dict = self._create_access_token_dict(
            user=user,
            user_session_id=user_session.id,
        )

        refresh_token_dict = await self._create_refresh_token_dict(
            user=user,
            user_session_id=user_session.id,
        )
        raw_refresh_token = refresh_token_dict.pop("refresh_token")

        access_token = await self.database.create(access_token_dict)
        refresh_token = await self.refresh_token_database.create(refresh_token_dict)  # noqa: F841

        return access_token.token, raw_refresh_token

    async def reissue_token(self, refresh_token: str, user_manager: BaseUserManager) -> tuple[str, str]:
        pass

    async def destroy_token(self, token: str, user: User, *, session_destroy: bool = False) -> None:
        access_token = await self.database.get_by_token(token)
        if access_token is not None:
            user_session = await self.user_session_database.get(access_token.session_id)
            if user_session is not None:
                if not session_destroy:
                    await self.user_session_database.revoke(user_session)
                    await self.database.delete(access_token)
                else:
                    await self.user_session_database.destroy(user_session)

    def _create_access_token_dict(
        self,
        user: User,
        user_session_id: int,
    ) -> dict[str, int, int]:
        token = token_urlsafe()
        return {
            "token": token,
            "session_id": user_session_id,
            "user_id": user.id,
        }

    async def _create_refresh_token_dict(
        self,
        user: User,
        user_session_id: int,
    ) -> dict[str, str, int, int]:
        refresh_token = token_urlsafe()

        hmac_fingerprint = await self._hmac_digest(
            key=settings.auth.refresh_token.hmac_secret,
            message=refresh_token,
            digestmod=hashlib.sha256,
        )

        return {
            "refresh_token": refresh_token,
            "fingerprint": hmac_fingerprint,
            "session_id": user_session_id,
            "user_id": user.id,
        }

    async def _hmac_digest(self, key: str, message: str, digestmod) -> str:
        hmac_ = hmac.new(
            key=key.encode(),
            msg=message.encode(),
            digestmod=digestmod,
        )

        return hmac_.hexdigest()

from datetime import datetime, timedelta, timezone

from fastapi_users import BaseUserManager, exceptions
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from core.models import AccessToken, User, UserSession, db_attach

from .exceptions_own import UserSessionInvalid


class StrategyOwn(DatabaseStrategy):
    def __init__(
        self,
        user_session: UserSession,
        database,
        lifetime_seconds=None,
    ):
        self.user_session = user_session
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
            await self._check_user_session(access_token=access_token)
            parsed_id = user_manager.parse_id(access_token.user_id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID, UserSessionInvalid):
            return None

    async def write_token(self, user: User) -> str:
        async with db_attach.session_factory() as session:
            user_session = UserSession(user_id=user.id)
            session.add(user_session)
            await session.commit()

        access_token_dict = self._create_access_token_dict(user)
        access_token_dict.update({"session_id": user_session.id})

        access_token = await self.database.create(access_token_dict)
        return access_token.token

    async def destroy_token(self, token: str, user: User, *, session_destroy: bool = True) -> None:
        access_token = await self.database.get_by_token(token)
        if access_token is not None:
            if session_destroy:
                async with db_attach.session_factory() as session:
                    user_session = await session.get(UserSession, access_token.session_id)
                    await session.delete(user_session)
                    await session.commit()
            else:
                await self.database.delete(access_token)

    async def _check_user_session(self, access_token: AccessToken) -> None:
        async with db_attach.session_factory() as session:
            user_session = await session.get(UserSession, access_token.session_id)

            if user_session.revoked_at:
                raise UserSessionInvalid

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AccessToken, User, UserSession

from .exceptions_own import UserSessionInvalid


class UserSessionDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_user_session(self, access_token: AccessToken) -> None:
        user_session = await self.session.get(UserSession, access_token.session_id)

        if user_session.revoked_at:
            raise UserSessionInvalid

    async def create_user_session(self, user: User) -> UserSession:
        user_session = UserSession(user_id=user.id)
        self.session.add(user_session)
        await self.session.commit()

        return user_session

    async def destroy_session(self, access_token: AccessToken) -> None:
        user_session = await self.session.get(UserSession, access_token.session_id)
        await self.session.delete(user_session)
        await self.session.commit()

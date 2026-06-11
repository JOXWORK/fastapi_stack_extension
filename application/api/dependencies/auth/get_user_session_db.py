from collections.abc import AsyncGenerator

from core.authentication.strategy_own import UserSessionDatabase
from core.models import db_attach
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_session_db(session: AsyncSession = Depends(db_attach.new_session)) -> AsyncGenerator[UserSessionDatabase]:
    yield UserSessionDatabase(session=session)

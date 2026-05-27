from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_attach


async def get_user_db(session: AsyncSession = Depends(db_attach.new_session)):
    yield SQLAlchemyUserDatabase(session, User)

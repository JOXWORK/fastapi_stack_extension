from core.models import db_attach
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .user import User


async def get_user_db(session: AsyncSession = Depends(db_attach.new_session)):
    yield SQLAlchemyUserDatabase(
        session=session,
        user_table=User,
    )

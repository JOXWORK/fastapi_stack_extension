from core.models import User, db_attach
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: AsyncSession = Depends(db_attach)):
    yield User.get_db(session=session)

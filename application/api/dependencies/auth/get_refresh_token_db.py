from core.authentication.own import RefreshTokenDatabase
from core.models import db_attach
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_refresh_token_db(session: AsyncSession = Depends(db_attach.new_session)):
    yield RefreshTokenDatabase(session=session)

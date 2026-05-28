from core.models import db_attach
from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .access_token import AccessToken


async def get_access_token_db(
    session: AsyncSession = Depends(db_attach.new_session),
):
    yield SQLAlchemyAccessTokenDatabase(
        session=session,
        access_token_table=AccessToken,
    )

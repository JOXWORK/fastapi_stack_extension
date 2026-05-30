from core.models import AccessToken, db_attach
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: AsyncSession = Depends(db_attach.new_session),
):
    yield AccessToken.get_db(session=session)

from __future__ import annotations

from typing import TYPE_CHECKING

from core.authentication.own import SQLAlchemyUserDatabaseOwn
from core.models import User, db_attach
from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: AsyncSession = Depends(db_attach.new_session)):
    yield SQLAlchemyUserDatabaseOwn(
        session=session,
        user_table=User,
    )

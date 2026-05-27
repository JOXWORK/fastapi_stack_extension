from fastapi import Depends

from core.models import get_user_db

from .user_manager import UserManager


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db=user_db)

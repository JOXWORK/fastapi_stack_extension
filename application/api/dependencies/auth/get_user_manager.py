from core.authentication import UserManager
from core.models import get_user_db
from fastapi import Depends


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db=user_db)

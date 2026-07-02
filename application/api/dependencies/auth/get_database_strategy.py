from core.authentication.own import RefreshTokenDatabase, StrategyOwn, UserSessionDatabase
from core.config import settings
from core.models import AccessToken
from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase

from .get_access_token_db import get_access_token_db
from .get_refresh_token_db import get_refresh_token_db
from .get_user_session_db import get_user_session_db


async def get_database_strategy(
    user_session_database: UserSessionDatabase = Depends(get_user_session_db),
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
    refresh_token_db: RefreshTokenDatabase = Depends(get_refresh_token_db),
) -> StrategyOwn:
    return StrategyOwn(
        user_session_database=user_session_database,
        database=access_token_db,
        refresh_token_database=refresh_token_db,
        lifetime_seconds=settings.auth.access_token.lifetime_seconds,
    )

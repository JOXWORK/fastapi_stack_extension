from core.authentication.strategy_own import StrategyOwn, UserSessionDatabase
from core.config import settings
from core.models import AccessToken
from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase

from .get_access_token_db import get_access_token_db
from .get_user_session_db import get_user_session_db


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
    user_session_database: UserSessionDatabase = Depends(get_user_session_db),
) -> StrategyOwn:
    return StrategyOwn(
        user_session_database=user_session_database,
        database=access_token_db,
        lifetime_seconds=settings.auth.access_token.lifetime_seconds,
    )

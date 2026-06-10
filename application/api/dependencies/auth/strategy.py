from core.authentication.strategy_own import StrategyOwn
from core.config import settings
from core.models import AccessToken, UserSession
from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase

from .get_access_token_db import get_access_token_db


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> StrategyOwn:
    return StrategyOwn(
        user_session=UserSession,
        database=access_token_db,
        lifetime_seconds=settings.auth.access_token.lifetime_seconds,
    )

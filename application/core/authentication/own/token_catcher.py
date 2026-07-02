from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi_users.types import DependencyCallable

    from core.models.access_token import AccessToken

    from .strategy_own import StrategyOwn


from fastapi import Depends, HTTPException, status

from .secure_schemes import http_scheme, oauth_scheme


def token_catcher(get_strategy: DependencyCallable[StrategyOwn]):
    async def _catch(
        strategy: StrategyOwn = Depends(get_strategy),
        token1: str = Depends(oauth_scheme),
        token2: str = Depends(http_scheme),
    ) -> AccessToken:
        token: str | None = None

        status_code = status.HTTP_401_UNAUTHORIZED
        if token1 is None and token2 is None:
            raise HTTPException(status_code=status_code)

        token = token1 or token2

        access_token = await strategy.read_token_ignore_expire(token=token)

        if access_token is None:
            raise HTTPException(status_code=status_code)

        return access_token

    return _catch

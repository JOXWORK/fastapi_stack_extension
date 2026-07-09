from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_users.authentication import AuthenticationBackend

if TYPE_CHECKING:
    from fastapi import Response
    from fastapi_users import BaseUserManager

    from core.models.user import User

    from .bearer_own import BearerTransportOwn
    from .strategy_own import StrategyOwn


class AuthenticationBackendOwn(AuthenticationBackend):
    def __init__(self, name, transport, get_strategy):
        super().__init__(name, transport, get_strategy)

        self.transport: BearerTransportOwn

    async def login(self, strategy: StrategyOwn, user: User) -> Response:
        access_token, refresh_token = await strategy.write_token(user)
        return await self.transport.get_login_response(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def reissue(self, strategy: StrategyOwn, user_manager: BaseUserManager, token: str) -> Response:
        access_token, refresh_token = await strategy.reissue_token(
            refresh_token=token,
            user_manager=user_manager,
        )

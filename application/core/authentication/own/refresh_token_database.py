from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from core.models.refresh_token import RefreshToken


class RefreshTokenDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_refresh_token(self, refresh_token_dict: dict[str, int, int]) -> RefreshToken:
        refresh_token = RefreshToken(**refresh_token_dict)
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)

        return refresh_token

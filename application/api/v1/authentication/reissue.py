from __future__ import annotations

from typing import TYPE_CHECKING

from core.schemas.authentication import TokenRefreshSchema
from fastapi import APIRouter, Depends

from api.dependencies.auth import get_token_catcher

if TYPE_CHECKING:
    from core.models import AccessToken

router = APIRouter()


@router.post("/reissue")
async def reissue(
    refresh_token: TokenRefreshSchema,
    access_token: AccessToken | None = Depends(get_token_catcher),
):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

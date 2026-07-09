from __future__ import annotations

from typing import TYPE_CHECKING

from core.schemas.authentication import TokenRefreshSchema
from fastapi import APIRouter

if TYPE_CHECKING:
    pass

router = APIRouter()


@router.post("/reissue")
async def reissue(
    refresh_token: TokenRefreshSchema,
):
    return {
        "refresh_token": refresh_token,
    }

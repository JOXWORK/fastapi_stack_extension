from __future__ import annotations

from typing import TYPE_CHECKING

from core.schemas.authentication import TokenRefreshSchema
from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies.auth import auth_backend, get_database_strategy, get_user_manager

if TYPE_CHECKING:
    from core.authentication.own import AuthenticationBackendOwn, BaseUserManagerOwn, StrategyOwn

router = APIRouter()


@router.post("/reissue")
async def reissue(
    token_schema: TokenRefreshSchema,
    strategy: StrategyOwn = Depends(get_database_strategy),
    user_manager: BaseUserManagerOwn = Depends(get_user_manager),
):
    response = await auth_backend.reissue(
        token=token_schema.refresh_token,
        strategy=strategy,
        user_manager=user_manager,
    )

    if response is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return response

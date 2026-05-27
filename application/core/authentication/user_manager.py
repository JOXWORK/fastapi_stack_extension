from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from core.config import settings
from core.models import User
from core.types_own.user_id import UserIdType

from .local_logger import user_manager_logger


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.auth.access_token.reset_password_token_secret
    verification_token_secret = settings.auth.access_token.verification_token_secret

    async def on_after_register(self, user: User, request: Request | None = None):
        user_manager_logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        user_manager_logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None):
        user_manager_logger.info(f"Verification requested for user {user.id}. Verification token: {token}")

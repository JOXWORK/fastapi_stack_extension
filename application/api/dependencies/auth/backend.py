from core.authentication import bearer_transport
from fastapi_users.authentication import AuthenticationBackend

from .get_database_strategy import get_database_strategy

auth_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

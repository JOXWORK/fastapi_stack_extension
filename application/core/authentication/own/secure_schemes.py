from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from core.config import settings

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.api.v1.prefix.bearer_transport,
    auto_error=settings.secure_schemes.oauth2_scheme,
)

http_scheme = HTTPBearer(auto_error=settings.secure_schemes.http_scheme)

from core.models.refresh_token import RefreshToken


class RefreshTokenWrapper:
    def __init__(self, model: RefreshToken, token: str):
        self.model = model
        self.token = token

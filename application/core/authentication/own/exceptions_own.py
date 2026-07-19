from fastapi_users.exceptions import FastAPIUsersException


class UserSessionInvalid(FastAPIUsersException):
    pass


class RefreshTokenRevoked(FastAPIUsersException):
    pass


class RefreshTokenUsed(FastAPIUsersException):
    pass


class RefreshTokenNotExeists(FastAPIUsersException):
    pass

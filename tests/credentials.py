from secrets import token_hex

mixin = token_hex(8)

username = f"test_{mixin}@e.com"
password = "qwerty"

credentials = {
    "register": {
        "email": username,
        "password": password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    },
    "login": {
        "username": username,
        "password": password,
    },
}

user_credentials = {
    "username": "user@e.com",
    "password": "ABBAB",
}

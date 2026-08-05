from secrets import token_hex

mixin = token_hex(8)

credentials = {
    "username": f"test_{mixin}@e.com",
    "password": "qwerty",
}

user_credentials = {
    "username": "user@e.com",
    "password": "ABBAB",
}

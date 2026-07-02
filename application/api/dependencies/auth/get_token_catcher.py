from core.authentication.own import token_catcher

from .get_database_strategy import get_database_strategy

get_token_catcher = token_catcher(get_strategy=get_database_strategy)

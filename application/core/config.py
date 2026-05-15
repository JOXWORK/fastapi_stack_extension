from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class HostSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

    uvc_reload: bool
    uvc_app_path: str = "main:app"
    uvc_workers: int


class ApiV1Prefix(BaseModel):
    router: str = "/v1"
    hello_world: str = "/hello_world"
    redis_cache_native: str = "/redis-cache-native"


class ApiPrefix(BaseModel):
    main_router: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class ApiV1Tags(BaseModel):
    hello_world: list[str] = ["Test routes"]
    redis_cache_native: list[str] = ["Redis cache native"]


class ApiV1Summary(BaseModel):
    hello_world: str = "This is a test router, take an order"


class ApiCustoms(BaseModel):
    prefix: ApiPrefix = ApiPrefix()
    tags: ApiV1Tags = ApiV1Tags()
    summary: ApiV1Summary = ApiV1Summary()


class DBSettings(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 20
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s:%(column_0_name)s__%(referred_table_name)s:%(referred_column_0_name)s",
        "pk": "pk_%(table_name)s_%(column_0_name)s",
    }


class RedisSettings(BaseModel):
    url: str
    ttl: int


class Settings(BaseSettings):
    ROOT_DIR: Path = ROOT_DIR

    model_config = SettingsConfigDict(
        env_file=(
            ".env.template",
            ".env",
        ),
        env_file_encoding="UTF-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APPLICATION__",
    )

    api: ApiCustoms = ApiCustoms()

    host: HostSettings

    db: DBSettings

    redis: RedisSettings


## Допустимо передовать в env_file кортеж из нескольких .env файлов, перегружающих друг друга и значения конфига.
## Например, env_file=(".env", ".env.template"). В .env указывается secrets информация, перегружая информацию из .env.template.
## Такой подход удобен для загрузки файлов конфига в репозиторий, не раскрывая secrets информацию.

settings = Settings()

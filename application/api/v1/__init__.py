from core.config import settings
from fastapi import APIRouter

from .hello_world.views import router as hello_world_router
from .redis_cache_native.views import router as redis_cache_native_router

router = APIRouter(prefix=settings.api.prefix.v1.router)


router.include_router(
    router=hello_world_router,
    tags=settings.api.tags.hello_world,
)

router.include_router(
    router=redis_cache_native_router,
    tags=settings.api.tags.redis_cache_native,
)

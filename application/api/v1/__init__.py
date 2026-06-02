from core.config import settings
from fastapi import APIRouter

from .hello_world.views import router as hello_world_router

router = APIRouter(prefix=settings.api.v1.prefix.router)
router.include_router(
    router=hello_world_router,
    tags=settings.api.v1.tags.hello_world,
)

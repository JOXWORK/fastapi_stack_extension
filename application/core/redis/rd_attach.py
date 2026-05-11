import redis.asyncio as redis

from core.config import settings


class RDAttach:
    def __init__(self):
        self.redis_client = redis.from_url(url=settings.redis.url)

    def get_redis(self):
        return self.redis_client

    async def aclose(self):
        await self.redis_client.aclose()


rd_attach = RDAttach()

import orjson
from core.config import settings
from core.models import Example, db_attach
from core.redis import rd_attach
from fastapi import Depends, HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import GetAnDbRowSchema, RedisExmapleJsonSchema


async def get_an_db_row_chached(
    example: GetAnDbRowSchema,
    redis: Redis = Depends(rd_attach.get_redis),
    session: AsyncSession = Depends(db_attach.new_session),
) -> dict[str, Example]:
    sub = await redis.get(f"{Example.__tablename__}:{example.id}")

    if sub:
        return {"cached": Example(**orjson.loads(sub))}

    obj = await session.get(entity=Example, ident=example.id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub with this id not found",
        )

    obj_val = RedisExmapleJsonSchema.model_validate(obj)
    sub = obj_val.model_dump_json()

    await redis.set(
        name=f"{Example.__tablename__}:{example.id}",
        value=sub,
        ex=settings.redis.ttl,
    )

    return {"main_db": obj}

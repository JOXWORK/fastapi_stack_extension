from core.config import settings
from core.models import Example, db_attach
from core.redis import rd_attach
from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ._async_decorator_test import callable_decorator, my_decorator
from .dependencies import get_an_db_row_chached
from .schemas import MyDecoratorSchema

router = APIRouter(prefix=settings.api.prefix.v1.redis_cache_native)


@router.post("/get-an-db-row")
async def getAndbRow(example_dict: dict[str, Example] = Depends(get_an_db_row_chached)) -> None:
    return example_dict


@router.post("/my-decorator-test")
@my_decorator
async def myDecoratorTest(example_schema: MyDecoratorSchema):
    return {"successful": True}


@router.post("/callable-decorator-test")
@callable_decorator(A=1, B=2)
async def callableDecoratorTest(example_schema: MyDecoratorSchema):
    return {"successful": True}

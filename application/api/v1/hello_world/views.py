from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.schemas import HelloWorldSchema
from core.models import db_attach

from .dependencies import (
    create_file_depends,
    check_file_exists,
    check_exists_and_get_content,
)
from .crud import (
    read_file,
    update_file,
    delete_file,
    create_row_example,
    get_row_example,
)

router = APIRouter(prefix=settings.api.prefix.v1.hello_world)


@router.get("/", summary=settings.api.summary.hello_world)
def root() -> str:
    return "Hello World!"


@router.post("/create_file")
def create_file_route(created: bool = Depends(create_file_depends)) -> dict:
    return {"success created": created}


@router.post("/read_file")
def read_file_route(path: str = Depends(check_file_exists)) -> str:
    content = read_file(path=path)
    return content


@router.post("/update_file")
def update_file_route(
    attributes: tuple = Depends(check_exists_and_get_content),
) -> dict:
    path = attributes[0]
    content = attributes[1]

    successful = update_file(
        path=path,
        content=content,
    )

    return {"success update": successful}


@router.delete("/delete_file")
def delete_file_route(path: str = Depends(check_file_exists)) -> dict:
    successful = delete_file(path=path)

    return {"success delete": successful}


@router.post("/hello_world_foo")
def hello_world_foo_router(hello_world: HelloWorldSchema):
    return {"successful": True}


@router.post("/create-an-db-row")
async def create_db_row_route(
    random_string_generation: bool = False,
    session: AsyncSession = Depends(db_attach.new_session),
):
    await create_row_example(
        random_string_generation=random_string_generation,
        session=session,
    )
    return {"success created": True}


@router.get("/get-an-db-row-example")
async def get_db_row_example(
    id: int,
    session: AsyncSession = Depends(db_attach.new_session),
):
    return await get_row_example(
        id=id,
        session=session,
    )

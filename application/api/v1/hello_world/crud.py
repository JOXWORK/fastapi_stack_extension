"""
Create
Read
Update
Delete
"""

from os import remove as file_remove
from random import choice
from string import ascii_letters, digits

from core.models import Example
from core.tasks import for_loop_task_example_task
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq.result.result import TaskiqResult


def create_file(path: str, content: str) -> bool:
    with open(path, "w") as file:
        file.write(content)
    return True


def read_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def update_file(path: str, content: str) -> bool:
    with open(path, "a") as file:
        file.write(content)

    return True


def delete_file(path: str) -> bool:
    file_remove(path)
    return True


def generate_random_string(length: int = 4):
    characters = ascii_letters + digits
    random_string = "".join([choice(characters) for i in range(length)])
    return random_string


async def create_row_example(random_string_generation: bool, session: AsyncSession):
    write_string = random_string_generation and generate_random_string(4) or "example"
    some_example = Example(example=write_string)

    session.add(some_example)
    await session.commit()


async def get_row_example(id: int, session: AsyncSession):
    return await session.get(
        entity=Example,
        ident=id,
    )


async def for_loop_task_example(stop: int) -> TaskiqResult:
    task = await for_loop_task_example_task.kiq(stop)
    result = await task.wait_result()

    return result

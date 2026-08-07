import pytest
from httpx import AsyncClient

from tests.conftest import url_root
from tests.credentials import credentials


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post(
        url=url_root + "/auth/register",
        json=credentials["register"],
    )

    assert response.status_code == 201

import orjson
import pytest
from httpx import AsyncClient

from tests.conftest import url_root
from tests.credentials import credentials


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    response = await client.post(
        url=url_root + "/auth/login",
        data=credentials["login"],
    )

    assert response.status_code == 200

    data = orjson.loads(response.text)

    assert "access_token" in data
    assert "refresh_token" in data

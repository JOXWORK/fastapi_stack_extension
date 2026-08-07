from __future__ import annotations

import orjson
import pytest_asyncio
from httpx import AsyncClient

from .credentials import credentials

url_root = "http://127.0.0.1:8000/api/v1"


@pytest_asyncio.fixture
async def client():
    async with AsyncClient() as client:
        yield client


@pytest_asyncio.fixture
async def token_pair(client: AsyncClient, login_credentials: dict):
    response = await client.post(
        url=url_root + "/auth/login",
        data=login_credentials,
    )

    assert response.status_code == 200

    data = orjson.loads(response.text)

    assert "access_token" in data
    assert "refresh_token" in data

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from credentials import credentials, user_credentials
from httpx import AsyncClient

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


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    response = await client.post(
        url=url_root + "/auth/register",
        # data=credentials,
        data={
            "username": "loluser@e.com",
            "password": "password",
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    response = await client.post(
        url=url_root + "/auth/login",
        data=credentials,
    )

    assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_login(token_pair: dict):
#     assert token_pair

#     print(token_pair)

#     assert "access_token" in token_pair
#     assert "refresh_token" in token_pair

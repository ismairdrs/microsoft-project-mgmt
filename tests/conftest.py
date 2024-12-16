import asyncio

import pytest
import pytest_asyncio
from aioresponses import aioresponses
from fastapi.testclient import TestClient
from httpx import AsyncClient

from microsoft.api import app

pytest_plugins = ("tests.fixtures.requests",)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_http():
    with aioresponses() as m:
        yield m


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test", timeout=None) as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

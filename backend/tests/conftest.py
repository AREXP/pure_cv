from aiohttp import web
import pytest

from backend import routes


@pytest.fixture
async def test_client(aiohttp_client):
    app = web.Application()
    app.add_routes(routes.routes)
    return await aiohttp_client(app)

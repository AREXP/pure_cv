import asyncio
from aiohttp import web
import json
import pathlib
import os

import pytest
import redis

from backend import config
from backend import init_db
from backend import routes


BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'config.test.json')


@pytest.fixture
async def test_client(aiohttp_client):
    app = web.Application()
    config.get_config(app, DEFAULT_CONFIG_PATH)
    app.add_routes(routes.routes)

    app.redis = redis.Redis(host='redis_test')

    app.on_startup.extend([init_db.init_database])
    app.on_cleanup.extend([init_db.close_database])

    return await aiohttp_client(app)

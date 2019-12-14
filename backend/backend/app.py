import argparse
import json
import pathlib
import os

from aiohttp import web
import asyncpg

from backend import handlers

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', default=DEFAULT_CONFIG_PATH)
    args, unknown = parser.parse_known_args()
    return args


def get_config(app: web.Application, config_path: str) -> web.Application:
    with open(config_path) as instream:
        config_str = instream.read()

    app.config = json.loads(config_str)


async def init_database(app: web.Application) -> None:
    pg_config = app.config['POSTGRES_DB_CONN']
    app.pg_pool = await asyncpg.create_pool(**pg_config)

async def close_database(app: web.Application) -> None:
    await app.pg_pool.close()


def init_app(argv=None) -> web.Application:
    app = web.Application()
    app.add_routes([
        web.get('/ping', handlers.ping_handler),
        web.post('/api/me', handlers.me_handler),
    ])

    args = parse_args()
    get_config(app, args.config_path)

    app.on_startup.extend([init_database])
    app.on_cleanup.extend([close_database])

    return app

# app = init_app()
web.run_app(init_app())

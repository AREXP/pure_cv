import argparse
import json
import pathlib
import os

from aiohttp import web
import asyncpg

from backend import config
from backend import routes
from backend import init_db

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', default=DEFAULT_CONFIG_PATH)
    args, unknown = parser.parse_known_args()
    return args


def init_app(argv=None) -> web.Application:
    app = web.Application()
    app.add_routes(routes.routes)

    args = parse_args()
    config.get_config(app, args.config_path)

    app.on_startup.extend([init_db.init_database])
    app.on_cleanup.extend([init_db.close_database])

    return app

# app = init_app()
web.run_app(init_app())

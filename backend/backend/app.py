import argparse
import json
import pathlib
import os

from aiohttp import web
import redis

from backend import config
from backend import routes
from backend import init_db

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
PORT = 8080


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', default=DEFAULT_CONFIG_PATH)
    args, unknown = parser.parse_known_args()
    return args


def init_app(argv=None) -> web.Application:
    args = parse_args()
    app = web.Application()
    app.add_routes(routes.routes)

    config.get_config(app, args.config_path)

    app.redis = redis.Redis(host='redis')

    app.on_startup.extend([init_db.init_database])
    app.on_cleanup.extend([init_db.close_database])

    return app

def main(argv=None):
    web.run_app(init_app(argv), port=PORT)

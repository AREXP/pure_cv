from aiohttp import web
import json


def get_config(app: web.Application, config_path: str) -> web.Application:
    with open(config_path) as instream:
        config_str = instream.read()

    app.config = json.loads(config_str)

from aiohttp import web
from backend import handlers

routes = [
    web.get('/ping', handlers.ping_handler),
    web.post('/api/me', handlers.me_handler),
]

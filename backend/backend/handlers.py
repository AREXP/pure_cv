import logging

from aiohttp import web

logger = logging.getLogger(__name__)


async def ping_handler(request):
    return web.Response(text='pong')

async def me_handler(request):
    return web.Response(text='me')

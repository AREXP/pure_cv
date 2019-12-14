import logging

from aiohttp import web

logger = logging.getLogger(__name__)


set_status_sql = """
INSERT INTO users (status, token)
VALUES ($1, $2)
ON CONFLICT (token)
DO UPDATE SET status = $1
"""

async def ping_handler(request):
    return web.Response(text='pong')

async def me_handler(request):
    data = await request.json()

    token = request.headers.get('token')
    if not token:
        return web.json_response({'msg': 'token is not provided'}, status=401)

    status = data.get('online')
    if status is None:
        return web.json_response(
            {'msg': 'online status is not provided'}, status=400,
        )

    async with request.app.pg_pool.acquire() as connection:
        await connection.execute(set_status_sql, status, token)
    logger.info('User %s set status to %s', token, status)

    return web.json_response({})

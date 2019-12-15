import datetime
import functools
import logging
import time

from aiohttp import web

logger = logging.getLogger(__name__)


EXPIRE_LIMITS = {
    'second': 1,
    'minute': 60,
    'hour': 3600,
}


def throttle(func):
    @functools.wraps(func)
    async def wrapper(request):
        logger.info('In wrapper!')
        token = request.headers.get('token')
        if not token:
            return web.json_response(
                {'msg': 'token is not provided'}, status=401,
            )

        data = await request.json()
        status = data.get('online')
        if status is None:
            return web.json_response(
                {'msg': 'online status is not provided'}, status=400,
            )

        limits = request.app.config['throttle_limits']
        now_time = datetime.datetime.utcnow()
        redis_client = request.app.redis
        for limit_type, limit in limits.items():
            time_key = getattr(now_time, limit_type)
            key = '{}:{}_{}'.format(token, limit_type, time_key)

            if not status:
                logger.debug('Erase key %s', key)
                redis_client.delete(key)
                continue

            current_value = redis_client.get(key)
            logger.debug('Key %s current value is %s', key, current_value)
            if current_value is not None and int(current_value) >= limit:
                return web.json_response(
                    {'msg': 'Rate limit is reached, try later'}, status=409,
                )
            with redis_client.pipeline() as pipe:
                pipe.incr(key)
                pipe.expire(key, EXPIRE_LIMITS[limit_type])
                pipe.execute()

            logger.debug('New key %s value is %s', key, redis_client.get(key))

        return await func(request)
    return wrapper

import os

from aiohttp import web
import asyncpg


async def migrate(app: web.Application) -> None:
    migrations_path = app.config['migrations_path']
    for address, sub_dirs, files in os.walk(migrations_path):
        for file_name in files:
            path = os.path.join(address, file_name)
            with open(path) as instream:
                migration = instream.read()

            async with app.pg_pool.acquire() as connection:
                await connection.execute(migration)

async def init_database(app: web.Application) -> None:
    pg_config = app.config['POSTGRES_DB_CONN']
    app.pg_pool = await asyncpg.create_pool(**pg_config)
    await migrate(app)


async def close_database(app: web.Application) -> None:
    await app.pg_pool.close()

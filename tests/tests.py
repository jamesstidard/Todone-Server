import pytest
import aiohttp
import asyncio
import rethinkdb as r
from todone import rethinkdb


@pytest.mark.asyncio
async def test_row_inset(app):
    connection = await rethinkdb.connection
    result = await r.table('test').insert([{"id": 0}, {"id": 1}, {"id": 2}]).run(connection)
    row = await r.table('test').get(0).run(connection)
    print(row)


async def fetch(session, url):
    with aiohttp.Timeout(100, loop=session.loop):
        async with session.get(url) as response:
            return await response.text()


@pytest.mark.asyncio
async def test():
    async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
        fetches = [fetch(session, 'http://localhost:8000/rpc/process') for _ in range(1000)]
        for result in asyncio.as_completed(fetches):
            print(await result)
        assert 0

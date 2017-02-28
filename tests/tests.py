import pytest

import rethinkdb as r
from hellosanic import rethinkdb


@pytest.mark.asyncio
async def test_row_inset(app):
    connection = await rethinkdb.connection
    result = await r.table('test').insert([{"id": 0}, {"id": 1}, {"id": 2}]).run(connection)
    row = await r.table('test').get(0).run(connection)
    print(row)

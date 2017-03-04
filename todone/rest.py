from sanic import Blueprint
from sanic.response import json

import rethinkdb as r

from todone.websocket import WebSocketClients


rest = Blueprint('rest', url_prefix='/rest')


@rest.get('/<resource:str>')
async def select(request, resource: str):
    # unwrap arg values from array for filter predicate
    predicate = {k: v[0] for k, v in request.args.items()}

    conn   = request.app.rdb_connection
    cursor = await r.table(resource).filter(predicate).run(conn)

    resources = []
    while await cursor.fetch_next():
        resources.append(await cursor.next())

    return json(resources)


@rest.post('/<resource>')
async def insert(request, resource: str):
    print(f'inserted {resource}')
    await WebSocketClients.broadcast('inserting')
    return json({'id': 12346, 'name': 'Jill'})


@rest.put('/<resource>')
async def update(request, resource: str):
    print(f'updated {resource}')
    await WebSocketClients.broadcast('updating')
    return json({'id': 12345, 'name': 'Jack'})


@rest.delete('/<resource>')
async def delete(request, resource: str):
    print(f'deleted {resource}')
    await WebSocketClients.broadcast('deleting')
    return json({'id': 54321})

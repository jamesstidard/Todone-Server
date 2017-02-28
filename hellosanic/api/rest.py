from sanic import Blueprint
from sanic.response import json

from ..websocket import broadcast


rest = Blueprint('rest', url_prefix='/rest')


@rest.get('/<resource>')
async def select(request, resource: str):
    print(f'selected {resource}', )
    await broadcast('selecting')
    return json({'id': 12345, 'name': 'Jack'})


@rest.post('/<resource>')
async def insert(request, resource: str):
    print(f'inserted {resource}')
    await broadcast('inserting')
    return json({'id': 12346, 'name': 'Jill'})


@rest.put('/<resource>')
async def update(request, resource: str):
    print(f'updated {resource}')
    await broadcast('updating')
    return json({'id': 12345, 'name': 'Jack'})


@rest.delete('/<resource>')
async def delete(request, resource: str):
    print(f'deleted {resource}')
    await broadcast('deleting')
    return json({'id': 54321})

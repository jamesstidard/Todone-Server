import asyncio

from inspect import isawaitable

from sanic.websocket import ConnectionClosed
from sanic.request import Request, json_loads
from sanic.response import json_dumps
from sanic.exceptions import ServerError, URLBuildError

ws_clients = set()


async def broadcast(message):
    broadcasts = [ws.send(message) for ws in ws_clients]
    if broadcasts:
        for result in asyncio.as_completed(broadcasts):
            try:
                await result
            except ConnectionClosed:
                pass


async def on_connect(request, ws):
    ws_clients.add(ws)
    while True:
        try:
            message = await ws.recv()
        except ConnectionClosed:
            ws_clients.remove(ws)
            break

        if message.startswith('select_'):
            handler = 'rest.select'
            method = 'GET'
            kwargs = {'resource': message[7:]}
        elif message.startswith('insert_'):
            handler = 'rest.insert'
            method = 'POST'
            kwargs = {'resource': message[7:]}
        elif message.startswith('update_'):
            handler = 'rest.update'
            method = 'PUT'
            kwargs = {'resource': message[7:]}
        elif message.startswith('delete_'):
            handler = 'rest.delete'
            method = 'DELETE'
            kwargs = {'resource': message[7:]}
        else:
            handler = f'rpc.{message}'
            method = 'POST'
            kwargs = {}

        try:
            url = request.app.url_for(handler, **kwargs)
        except URLBuildError:
            await ws.send(json_dumps({
                'request_id': 0,
                'result': None,
                'error': 404,
                'message': 'Unknown endpoint with name and kwargs'}))
        else:
            faux_request = Request(url_bytes=str.encode(url),
                                   transport=request.transport,
                                   headers=request.headers,
                                   version=request.version,
                                   method=method)
            handler, args, kwargs = request.app.router.get(faux_request)

            # noinspection PyBroadException
            try:
                response = handler(request, *args, **kwargs)
                if isawaitable(response):
                    response = await response
            except ServerError as e:
                await ws.send(json_dumps({
                    'request_id': 0,
                    'result': None,
                    'error': e.status_code,
                    'message': e.args[0]}))
            except Exception:
                await ws.send(json_dumps({
                    'request_id': 0,
                    'result': None,
                    'error': 500,
                    'message': 'Internal Server Error'}))
            else:
                await ws.send(json_dumps({
                    'request_id': 0,
                    'result': json_loads(response.body),
                    'error': None,
                    'message': None}))

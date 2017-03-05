import asyncio

from inspect import isawaitable

from multiprocessing import Manager

from sanic.websocket import ConnectionClosed, WebSocketCommonProtocol
from sanic.request import Request, json_loads
from sanic.response import json_dumps
from sanic.exceptions import ServerError, URLBuildError


class WebSocketClients:
    # Clients are managed as a linked list
    # unauthed clients stored as hash(websocket): None
    # auths clients have two entries hash(websocket): user_uuid and user_id: websocket for quick access
    __clients = {}

    @classmethod
    def add(cls, client, *, user_uuid=None):
        if user_uuid:
            cls.__clients[client] = user_uuid
            cls.__clients[user_uuid] = client
        else:
            cls.__clients[client] = None

    @classmethod
    def remove(cls, client):
        uuid = cls.__clients.pop(client, None)
        cls.__clients.pop(uuid, None)

    @classmethod
    def auth(cls, client, *, user_uuid):
        cls.__clients[client] = user_uuid
        cls.__clients[user_uuid] = client

    @classmethod
    def unauth(cls, client):
        uuid = cls.__clients.get(client, None)
        cls.__clients.pop(uuid, None)

    @classmethod
    async def broadcast(cls, message, *uuids):
        public = not uuids
        if public:
            broadcasts = [ws.send(message) for ws, _ in cls.__clients.items()
                          if isinstance(ws, WebSocketCommonProtocol)]
        else:
            broadcasts = [ws.send(message) for uuid, ws in cls.__clients.items()
                          if isinstance(ws, WebSocketCommonProtocol)
                          and uuid in uuids]
        if broadcasts:
            for result in asyncio.as_completed(broadcasts):
                try:
                    await result
                except ConnectionClosed:
                    pass


async def on_connect(request, ws):
    request.app.websocket_clients.add(ws)
    while True:
        try:
            message = await ws.recv()
        except ConnectionClosed:
            request.app.websocket_clients.remove(ws)
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
                # TODO: handle streamed response type
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

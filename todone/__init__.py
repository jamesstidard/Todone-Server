import asyncio

from sanic import Sanic
from sanic_rethinkdb import RethinkDB

from todone.rpc import rpc
from todone.rest import rest
from todone.model import SCHEMA
from todone.websocket import on_connect, WebSocketClients
from todone.broadcasts import subscribe_and_broadcast
from todone.utils import wait


def create_app(config):
    app = Sanic(__name__)
    app.config.from_object(config)

    rethinkdb = RethinkDB(app)

    if app.config.DROP_REMAKE_DB and input('Really drop the DB? (y/N)').lower() == 'y':
        wait(rethinkdb.drop_and_remake(SCHEMA))

    app.blueprint(rpc)
    app.blueprint(rest)

    app.add_websocket_route(on_connect, '/websocket')

    @app.listener('before_server_start')
    async def before_server_start(app_, loop):
        # Per process specific setup
        app_.rdb_connection = await rethinkdb.connection()
        app_.websocket_clients = WebSocketClients()
        loop.create_task(subscribe_and_broadcast(app_))

    return app

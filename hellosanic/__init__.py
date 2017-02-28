from sanic import Sanic
from sanic_rethinkdb import RethinkDB

from hellosanic.websocket import on_connect

rethinkdb = RethinkDB()


def create_app():
    app = Sanic(__name__)
    app.config.LOGO = ''

    rethinkdb.init_app(app)

    app.add_websocket_route(on_connect, '/websocket')

    return app

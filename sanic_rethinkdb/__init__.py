import rethinkdb as r

r.set_loop_type('asyncio')


class RethinkDB:

    def __init__(self, app=None):
        self.app = app
        self.connection = r.connect

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('RETHINKDB_HOST', 'localhost')
        app.config.setdefault('RETHINKDB_PORT', '28015')
        app.config.setdefault('RETHINKDB_AUTH', '')
        app.config.setdefault('RETHINKDB_DB', 'test')

        self.connection = r.connect(auth_key=app.config.RETHINKDB_AUTH,
                                    host=app.config.RETHINKDB_HOST,
                                    port=app.config.RETHINKDB_PORT,
                                    db=app.config.RETHINKDB_DB)

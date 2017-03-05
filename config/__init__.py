import os

from sanic_envconfig import EnvConfig


class Config(EnvConfig):
    LOGO: str = ''
    DEBUG: bool = False
    PORT: int = 8000
    WORKERS: int = os.cpu_count()

    RETHINKDB_HOST = 'localhost'
    RETHINKDB_PORT = '28015'
    RETHINKDB_AUTH = ''
    RETHINKDB_DB = 'todone'
    DROP_REMAKE_DB = False

    AMQP_HOST = 'localhost'
    AMQP_PORT = 5672
    AMQP_USERNAME = ''
    AMQP_PASSWORD = ''

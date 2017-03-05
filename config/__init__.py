import os

from sanic_envconfig import EnvConfig


class Config(EnvConfig):
    LOGO: str = ''
    DEBUG: bool = False
    PORT: int = 8000
    WORKERS: int = os.cpu_count()

    DROP_REMAKE_DB: bool = False
    RETHINKDB_HOST: str = 'localhost'
    RETHINKDB_PORT: str = '28015'
    RETHINKDB_DB: str = 'todone'
    RETHINKDB_AUTH: str = None
    RETHINKDB_USER: str = 'admin'
    RETHINKDB_PASSWORD: str = ''

    AMQP_HOST: str = 'localhost'
    AMQP_PORT: int = 32774
    AMQP_USERNAME: str = 'guest'
    AMQP_PASSWORD: str = 'guest'

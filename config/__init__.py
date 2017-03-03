from sanic_envconfig import EnvConfig


class Config(EnvConfig):
    LOGO: str = ''
    DEBUG: bool = False
    PORT: int = 8000
    WORKERS: int = 4

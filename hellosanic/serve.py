from config import Config
from hellosanic import create_app


if __name__ == '__main__':
    app = create_app(Config)
    app.run(host="0.0.0.0", port=Config.PORT,  debug=Config.DEBUG, workers=Config.WORKERS)

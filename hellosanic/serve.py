from hellosanic import create_app
from hellosanic.api import rest, rpc


if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(rpc)
    app.register_blueprint(rest)
    app.run(host="0.0.0.0", port=8000, debug=True)

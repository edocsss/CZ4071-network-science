from flask import Flask
from http_handlers import graph_handler


def make_app():
    return Flask(__name__)


def setup_blueprints(app):
    app.register_blueprint(graph_handler.blueprint)


if __name__ == '__main__':
    app = make_app()
    setup_blueprints(app)
    app.run(debug=True, port=3000)
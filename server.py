from flask import Flask
from http_handlers import graph_handler


app = Flask(__name__)


def setup_blueprints(app):
    app.register_blueprint(graph_handler.blueprint)


@app.after_request
def cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response


if __name__ == '__main__':
    setup_blueprints(app)
    app.run(debug=True, port=3000, threaded=True)
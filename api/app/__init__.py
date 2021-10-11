import os

from flask import Flask
from flask_cors import CORS

from app.routes import route
from app.config import config, init_config


def create_flask_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    route(app)

    path = os.environ.get('CONFIG_PATH') if os.environ.get(
        'CONFIG_PATH') else "./settings.ini"
    init_config(path)
    try:
        app.config.update(dict(
            SECRET_KEY=str(config['FLASK_APP']['FLASK_APP_SECRET_KEY'])
        ))
        print(f"\nServer started with config {path}\n")
    except KeyError:
        print(f"\nFile {path} not found or invlalid\n")

    return app

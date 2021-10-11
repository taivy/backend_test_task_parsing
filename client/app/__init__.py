import os

from flask import Flask

from app.routes import route
from app.config import config, init_config


def create_flask_app():
    app = Flask(__name__, template_folder='../templates')

    route(app)

    path = os.environ.get('CONFIG_PATH') if os.environ.get(
        'CONFIG_PATH') else "./settings.ini"
    init_config(path)
    try:
        app.config.update(dict(
            SECRET_KEY=str(config['FLASK_APP']['FLASK_APP_SECRET_KEY']),
            CSRF_ENABLED=bool(config['FLASK_APP']['CSRF_ENABLED']),
            API_URL=str(config['API']['API_URL']),
            API_REQUESTS_TIMEOUT=int(config['API']['API_REQUESTS_TIMEOUT']),
        ))
        print(f"\nServer started with config {path}\n")
    except (KeyError, ValueError):
        print(f"\nFile {path} not found or invlalid\n")

    return app

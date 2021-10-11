from modules.api import api_bp


def route(app):
    app.register_blueprint(api_bp)

from modules.people_search import people_search_bp


def route(app):
    app.register_blueprint(people_search_bp)

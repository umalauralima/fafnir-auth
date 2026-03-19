from .auth_routes import auth_bp

def register_blueprints(app):

    blueprints = [
        auth_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)
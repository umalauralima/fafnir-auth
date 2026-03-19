from flask import Flask
from app.routes import register_blueprints
from .config import Config
from .extensions import db, migrate

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    from app import models

    return app

## flask db init - inicializar os migrates
## flask db migrate -m "initial tables" --- cria o migrate
## flask db upgrade ----- aplica no banco
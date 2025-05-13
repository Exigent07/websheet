from flask import Flask
from .config import Config
from .database import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app

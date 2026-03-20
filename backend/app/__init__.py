from flask import Flask
from .config import Config
from .extensions import init_extensions

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
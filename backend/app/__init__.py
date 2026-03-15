from flask import Flask
from .config import Config
from .extensions import db
from .routes import api_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(api_bp)

    return app
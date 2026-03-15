from flask import Flask
from .config import Config
from .extensions import db, jwt, init_extensions
from .routes import api_bp, setup_scheduler

def create_app(config_class=Config):
    app = Flask(__name__)
    init_extensions(app)

    app.register_blueprint(api_bp, url_prefix='/api')
    setup_scheduler()

    return app
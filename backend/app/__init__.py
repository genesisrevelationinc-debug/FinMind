from flask import Flask
from .config import Config
from .extensions import init_extensions, register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_extensions(app)
    register_routes(app)
    return app
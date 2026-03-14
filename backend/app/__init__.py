from flask import Flask
from .extensions import db, jwt, scheduler
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.app.config.Config')
    init_extensions(app)
    register_routes(app)
    return app
from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .extensions import db
from .routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(api_bp)

    return app
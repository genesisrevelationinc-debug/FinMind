from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .routes import api_bp
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.app.config.Config')

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(api_bp)

    return app
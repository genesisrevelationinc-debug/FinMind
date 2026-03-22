from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config
from .extensions import db
from .routes import auth
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(accounts.accounts_bp)

    return app
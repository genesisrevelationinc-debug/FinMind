from flask import Flask
from .config import Config
from .routes.accounts import accounts_bp
from .extensions import db, jwt
from .routes import auth

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(accounts_bp)

    return app
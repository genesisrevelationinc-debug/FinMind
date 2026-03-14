from flask import Flask
from .config import Config
from .routes.insights import insights_bp
from .extensions import db, jwt
from .routes import auth, expenses, bills, reminders

    app.register_blueprint(auth.bp)
    app.register_blueprint(expenses.bp)
    app.register_blueprint(bills.bp)
    app.register_blueprint(insights_bp)
    app.register_blueprint(reminders.bp)

    return app
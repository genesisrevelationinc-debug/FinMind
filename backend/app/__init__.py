from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_webhook import Webhook

db = SQLAlchemy()
def create_app():
    app.config.from_object('backend.app.config.Config')
    db.init_app(app)

    webhook = Webhook(app)
    webhook.init_app(app)

    from backend.app.webhooks import register_webhooks
    register_webhooks(webhook)

    from backend.app.routes import auth
    app.register_blueprint(auth.bp)

    return app
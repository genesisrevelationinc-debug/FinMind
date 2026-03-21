from flask import Flask
from .routes import api_bp
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    app.register_blueprint(api_bp)

    return app
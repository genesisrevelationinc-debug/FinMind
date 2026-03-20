from flask import Flask
from .extensions import db
from .routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    app.register_blueprint(api_bp)

    return app

# Initialize other extensions here if needed
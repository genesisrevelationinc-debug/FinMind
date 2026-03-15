from flask import Flask
from .config import Config
from .extensions import init_extensions, db, scheduler
from .routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_bp)

    return app

def monitor_jobs():
    # Logic to monitor and retry jobs
    pass
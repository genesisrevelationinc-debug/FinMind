from flask import Flask
from .extensions import scheduler, init_scheduler, shutdown_scheduler
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_scheduler(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        shutdown_scheduler()
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

db = SQLAlchemy()
scheduler = APScheduler()

def init_extensions(app):
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # Configure job defaults
    scheduler.api_enabled = True
    scheduler.add_job(id='monitor_jobs', func=monitor_jobs, trigger='interval', seconds=300)
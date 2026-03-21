from flask import Blueprint
from apscheduler.triggers.cron import CronTrigger
from ..extensions import scheduler
from .auth import auth_bp
from .expenses import expenses_bp
from .bills import bills_bp
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(bills_bp, url_prefix='/bills')
    app.register_blueprint(reminders_bp, url_prefix='/reminders')
    app.register_blueprint(insights_bp, url_prefix='/insights')

    # Example of scheduling a job
    def example_job():
        print("Running example job")

    scheduler.add_job(example_job, CronTrigger.from_crontab('0 0 * * *'))  # Daily at midnight
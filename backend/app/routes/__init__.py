from flask import Blueprint
from . import auth
from ..extensions import scheduler

def register_routes(app):
    app.register_blueprint(auth.bp)
    # Example of adding a scheduled job
    # scheduler.add_job(func=some_function, trigger='interval', seconds=60, id='job_id', replace_existing=True)
from flask import Blueprint
from . import auth
from ..extensions import scheduler

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(auth.bp, url_prefix='/auth')

def setup_scheduler():
    from ..jobs import reminder_job
    scheduler.add_job(
        id='reminder_job',
        func=reminder_job.run,
        trigger='interval',
        minutes=30
    )
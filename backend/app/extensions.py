from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED
import logging

logger = logging.getLogger(__name__)

def job_error_listener(event):
    logger.error(f"Job {event.job_id} failed with exception: {event.exception}")

def job_missed_listener(event):
    logger.warning(f"Job {event.job_id} missed its scheduled run")

def init_scheduler(app):
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(20)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=app.config['TIMEZONE'])
    scheduler.add_listener(job_error_listener, EVENT_JOB_ERROR)
    scheduler.add_listener(job_missed_listener, EVENT_JOB_MISSED)
    scheduler.start()
    app.scheduler = scheduler
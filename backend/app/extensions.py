from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import logging

db = SQLAlchemy()
jwt = JWTManager()

scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()},
                              executors={'default': ThreadPoolExecutor(20)},
                              job_defaults={'coalesce': False, 'max_instances': 3},
                              timezone="UTC")
scheduler.add_listener(lambda event: logging.info(f"Job {event.job_id} failed with exception {event.exception}"), scheduler.events.EVENT_JOB_ERROR)
scheduler.start()
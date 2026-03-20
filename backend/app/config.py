import os

class Config:
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    DEBUG = os.environ.get('DEBUG', False)

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/finmind')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis Config
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    # APScheduler Config
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {
        'default': {
            'type': 'redis',
            'url': REDIS_URL,
            'job_defaults': {
                'coalesce': False,
                'max_instances': 3
            }
        }
    }
    SCHEDULER_EXECUTORS = {
        'default': {
            'type': 'threadpool',
            'max_workers': 20
        }
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }
    SCHEDULER_TIMEZONE = 'UTC'
import os

class Config:
    """Base configuration."""
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {
        'default': {
            'type': 'redis',
            'url': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        }
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {'coalesce': False, 'max_instances': 3}
import os

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/finmind')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    APSCHEDULER_JOBSTORES = {
        'default': {
            'type': 'redis',
            'url': REDIS_URL,
        }
    }
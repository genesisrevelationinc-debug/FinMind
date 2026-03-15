import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///finmind.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'UTC'
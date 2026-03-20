import os

class Config:
    WEBHOOK_SECRET_KEY = os.environ.get('WEBHOOK_SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///finmind.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
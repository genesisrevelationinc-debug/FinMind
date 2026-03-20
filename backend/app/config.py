import os

class Config:
    WEBHOOK_SECRET_KEY = os.getenv('WEBHOOK_SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///finmind.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
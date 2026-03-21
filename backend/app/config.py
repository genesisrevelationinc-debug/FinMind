import os
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    TIMEZONE = timezone(os.getenv('TIMEZONE', 'UTC'))
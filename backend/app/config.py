import os
from dotenv import load_dotenv
import logging

load_dotenv()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    logging.basicConfig(level=getattr(logging, LOGGING_LEVEL.upper(), logging.INFO))
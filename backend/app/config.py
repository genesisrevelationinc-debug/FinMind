import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

load_dotenv()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default_webhook_secret')
    WEBHOOK_PRIVATE_KEY = serialization.load_pem_private_key(
        os.getenv('WEBHOOK_PRIVATE_KEY').encode(),
        password=None,
    )
    WEBHOOK_PUBLIC_KEY = serialization.load_pem_public_key(
        os.getenv('WEBHOOK_PUBLIC_KEY').encode(),
    )
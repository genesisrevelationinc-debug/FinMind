from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import logging

db = SQLAlchemy()


def init_extensions(app: Flask):
    db.init_app(app)

    # Setup audit logging
    global audit_log
    audit_log = logging.getLogger('audit')
    handler = logging.FileHandler('audit.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    audit_log.addHandler(handler)
    audit_log.setLevel(logging.INFO)
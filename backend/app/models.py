from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from ..extensions import db
from ..config import Config
from ..utils import send_email
from .routes.auth import AuditLog


class User(db.Model):
        "id": self.id,
        "user_id": self.user_id,
        "message": self.message,
        "due_date": self.due_date,
        "channel": self.channel
    }


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog {self.id}>"
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class User(db.Model):
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)
    bills = db.relationship('Bill', backref='user', lazy=True)
    reminders = db.relationship('Reminder', backref='user', lazy=True)

    def to_dict(self):
        return {
        }


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        }


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    channel = db.Column(db.String(50), nullable=False)


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        }

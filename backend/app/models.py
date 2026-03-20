from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timedelta
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    accounts = relationship('Account', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'balance': self.balance
        }

class Expense(db.Model):
    __tablename__ = 'expenses'

    category = db.Column(db.String(150), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)

class Bill(db.Model):
    __tablename__ = 'bills'
    cadence = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    channel = db.Column(db.String(50), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)

class Reminder(db.Model):
    __tablename__ = 'reminders'
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=False)

class Bill(db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    cadence = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    channel = db.Column(db.String(50), nullable=False)
    paid = db.Column(db.Boolean, default=False)
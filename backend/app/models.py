from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Expense(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(Date, default=datetime.utcnow)
    user = relationship('User', backref=db.backref('expenses', lazy=True))

class Bill(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    user = relationship('User', backref=db.backref('bills', lazy=True))

    def __repr__(self):
        return f'<Bill {self.name}>'
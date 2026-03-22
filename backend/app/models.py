from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

db = SQLAlchemy()

    categories = relationship('Category', back_populates='user')
    expenses = relationship('Expense', back_populates='user')
    bills = relationship('Bill', back_populates='user')

class Account(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    balance = Column(Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'balance': self.balance
        }
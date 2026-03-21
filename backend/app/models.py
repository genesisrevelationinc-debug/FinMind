from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .extensions import db
from datetime import date

class SavingsGoal(db.Model):
    __tablename__ = 'savings_goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_name = Column(String(255), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    start_date = Column(Date, default=date.today)
    end_date = Column(Date, nullable=True)
    user = relationship('User', back_populates='savings_goals')

class Milestone(db.Model):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True)
    savings_goal_id = Column(Integer, ForeignKey('savings_goals.id'), nullable=False)
    milestone_name = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    achieved = Column(Boolean, default=False)
    savings_goal = relationship('SavingsGoal', back_populates='milestones')

class User(db.Model):
    __tablename__ = 'users'
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    expenses = relationship('Expense', back_populates='user')
    savings_goals = relationship('SavingsGoal', back_populates='user')

class Expense(db.Model):
    __tablename__ = 'expenses'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='expenses')

User.savings_goals = relationship('SavingsGoal', order_by=SavingsGoal.id, back_populates='user')
SavingsGoal.milestones = relationship('Milestone', order_by=Milestone.id, back_populates='savings_goal')
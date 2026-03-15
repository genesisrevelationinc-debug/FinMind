from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .extensions import db

class SavingsGoal(db.Model):
    __tablename__ = 'savings_goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    description = Column(String(255))

    user = relationship('User', back_populates='savings_goals')

class Milestone(db.Model):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True)
    savings_goal_id = Column(Integer, ForeignKey('savings_goals.id'), nullable=False)
    name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255))

    savings_goal = relationship('SavingsGoal', back_populates='milestones')

User.savings_goals = relationship('SavingsGoal', order_by=SavingsGoal.id, back_populates='user')
SavingsGoal.milestones = relationship('Milestone', order_by=Milestone.id, back_populates='savings_goal')
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SavingsGoal(Base):
    __tablename__ = 'savings_goals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    due_date = Column(Date, nullable=False)
    user = relationship("User", back_populates="savings_goals")

class Milestone(Base):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True, index=True)
    savings_goal_id = Column(Integer, ForeignKey('savings_goals.id'), nullable=False)
    milestone_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    achieved = Column(Boolean, default=False)
    savings_goal = relationship("SavingsGoal", back_populates="milestones")

class User(Base):
    __tablename__ = 'users'
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    categories = relationship("Category", back_populates="owner")
    savings_goals = relationship("SavingsGoal", back_populates="user")

class Category(Base):
    __tablename__ = 'categories'
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")

SavingsGoal.milestones = relationship("Milestone", order_by=Milestone.id, back_populates="savings_goal")
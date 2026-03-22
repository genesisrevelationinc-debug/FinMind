from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class SavingsGoal(Base):
    __tablename__ = 'savings_goals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="savings_goals")

class Milestone(Base):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True, index=True)
    savings_goal_id = Column(Integer, ForeignKey('savings_goals.id'), nullable=False)
    milestone_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    achieved = Column(Boolean, default=False)
    savings_goal = relationship("SavingsGoal", back_populates="milestones")
from . import auth
from . import savings
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import SavingsGoal, Milestone
from ..schemas import SavingsGoalCreate, SavingsGoalUpdate, MilestoneCreate, MilestoneUpdate

router = APIRouter(prefix="/savings", tags=["Savings"])

@router.post("/goals/", response_model=SavingsGoalCreate)
def create_savings_goal(goal: SavingsGoalCreate, db: Session = Depends(get_db)):
    db_goal = SavingsGoal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/goals/{goal_id}", response_model=SavingsGoalCreate)
def read_savings_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id).first()
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Savings goal not found")
    return db_goal

@router.put("/goals/{goal_id}", response_model=SavingsGoalUpdate)
def update_savings_goal(goal_id: int, goal: SavingsGoalUpdate, db: Session = Depends(get_db)):
    db_goal = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id).first()
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Savings goal not found")
    for key, value in goal.dict(exclude_unset=True).items():
        setattr(db_goal, key, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.post("/goals/{goal_id}/milestones/", response_model=MilestoneCreate)
def create_milestone(goal_id: int, milestone: MilestoneCreate, db: Session = Depends(get_db)):
    db_milestone = Milestone(savings_goal_id=goal_id, **milestone.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.get("/milestones/{milestone_id}", response_model=MilestoneCreate)
def read_milestone(milestone_id: int, db: Session = Depends(get_db)):
    db_milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if db_milestone is None:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return db_milestone

@router.put("/milestones/{milestone_id}", response_model=MilestoneUpdate)
def update_milestone(milestone_id: int, milestone: MilestoneUpdate, db: Session = Depends(get_db)):
    db_milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if db_milestone is None:
        raise HTTPException(status_code=404, detail="Milestone not found")
    for key, value in milestone.dict(exclude_unset=True).items():
        setattr(db_milestone, key, value)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone
from pydantic import BaseModel
from typing import Optional

class SavingsGoalCreate(BaseModel):
    user_id: int
    goal_name: str
    target_amount: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class SavingsGoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class MilestoneCreate(BaseModel):
    milestone_name: str
    amount: float
    achieved: Optional[bool] = False
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models import SavingsGoal, Milestone
from .config import settings
from .models import User, Category, Expense, Bill, Reminder, AdImpression, SubscriptionPlan, UserSubscription, RefreshToken, AuditLog
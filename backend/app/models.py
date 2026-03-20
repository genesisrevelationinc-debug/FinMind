from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    audit_logs = relationship('AuditLog', backref='user', lazy=True)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    login_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(String(255), nullable=False)
    success = Column(Boolean, default=True)
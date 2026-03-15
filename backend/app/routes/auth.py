from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db, AuditLog
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    audit_log = AuditLog(action="User Registration", user_id=None, details=str(data))
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    audit_log.user_id = new_user.id
    db.session.add(audit_log)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201
@auth_bp.route('/login', methods=['POST'])
    return jsonify({'message': 'Invalid credentials'}), 401
@auth_bp.route('/export-data', methods=['GET'])
@jwt_required()
def export_data():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = {
        'username': user.username,
        'email': user.email,
        'expenses': [expense.to_dict() for expense in user.expenses],
        'bills': [bill.to_dict() for bill in user.bills],
        'reminders': [reminder.to_dict() for reminder in user.reminders]
    }
    audit_log = AuditLog(action="Data Export", user_id=user_id, details="Exported user data")
    db.session.add(audit_log)
    db.session.commit()
    return jsonify(user_data), 200

@auth_bp.route('/delete-data', methods=['DELETE'])
@jwt_required()
def delete_data():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    audit_log = AuditLog(action="Data Deletion", user_id=user_id, details="Deleted user data")
    db.session.delete(user)
    db.session.add(audit_log)
    db.session.commit()
    return jsonify({'message': 'User data deleted successfully'}), 200

@auth_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
def get_audit_logs():
    user_id = get_jwt_identity()
    audit_logs = AuditLog.query.filter_by(user_id=user_id).all()
    logs = [{'action': log.action, 'timestamp': log.timestamp, 'details': log.details} for log in audit_logs]
    return jsonify(logs), 200

--- a/backend/app/models.py
@@ -1,4 +1,5 @@
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)
    bills = db.relationship('Bill', backref='user', lazy=True)
    reminders = db.relationship('Reminder', backref='user', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)

    def to_dict(self):
        return {
            'expenses': [expense.to_dict() for expense in self.expenses]
        }

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            'details': self.details
        }
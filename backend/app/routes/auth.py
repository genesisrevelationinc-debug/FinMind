from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from ..models import User, RefreshToken
from ..extensions import mail, jwt
from ..config import Config
from ..extensions import db
from ..utils import send_email
auth_bp = Blueprint('auth', __name__)
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/export_data', methods=['GET'])
@jwt_required()
def export_data():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "expenses": [expense.to_dict() for expense in user.expenses],
        "bills": [bill.to_dict() for bill in user.bills],
        "reminders": [reminder.to_dict() for reminder in user.reminders]
    }

    return jsonify(user_data), 200


@auth_bp.route('/delete_data', methods=['DELETE'])
@jwt_required()
def delete_data():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Log the deletion in audit_logs
    audit_log = AuditLog(user_id=user_id, action="DELETE_USER_DATA")
    db.session.add(audit_log)

    # Delete user data
    for expense in user.expenses:
        db.session.delete(expense)
    for bill in user.bills:
        db.session.delete(bill)
    for reminder in user.reminders:
        db.session.delete(reminder)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User data deleted successfully"}), 200


@auth_bp.route('/audit_logs', methods=['GET'])
@jwt_required()
def get_audit_logs():
    user_id = get_jwt_identity()
    audit_logs = AuditLog.query.filter_by(user_id=user_id).all()
    if not audit_logs:
        return jsonify({"message": "No audit logs found"}), 404

    logs = [{"id": log.id, "user_id": log.user_id, "action": log.action, "timestamp": log.timestamp} for log in audit_logs]
    return jsonify(logs), 200


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "timestamp": self.timestamp
        }
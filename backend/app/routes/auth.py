from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models import User, AuditLog
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/login', methods=['POST'])
def login():
    session: Session = db.session
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
        return jsonify({"msg": "Bad username or password"}), 401

    user.last_login = datetime.utcnow()
    user.login_attempts = 0  # Reset login attempts on successful login
    session.add(user)
    session.commit()

    # Log the login activity
    audit_log = AuditLog(user_id=user.id, activity='Login successful')
    session.add(audit_log)
    session.commit()

    # Check for suspicious login activity
    recent_logins = session.query(AuditLog).filter(
        AuditLog.user_id == user.id,
        AuditLog.timestamp > datetime.utcnow() - timedelta(minutes=5)
    ).count()

    if recent_logins > 5:
        return jsonify({"msg": "Suspicious login activity detected. Please contact support."}), 403

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)
def register():
    data = request.get_json()
    username = data.get('username')
    session: Session = db.session
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400
    db.session.add(new_user)
    db.session.commit()

    # Log the registration activity
    audit_log = AuditLog(user_id=new_user.id, activity='User registered')
    session.add(audit_log)
    session.commit()
    return jsonify({"msg": "User created successfully"}), 201
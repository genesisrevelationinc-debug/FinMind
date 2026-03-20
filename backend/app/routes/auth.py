from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db, AuditLog
from app.extensions import jwt
        return jsonify({"msg": "Bad username or password"}), 401

    user.last_login = datetime.utcnow()
    user.login_attempts = 0
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({"msg": "Bad username or password"}), 401

@auth.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.json.get('username')).first()
    if not user or not check_password_hash(user.password_hash, request.json.get('password')):
        user.login_attempts += 1
        db.session.add(user)
        db.session.commit()
        if user.login_attempts >= 5:
            audit_log = AuditLog(user_id=user.id, activity='Suspicious login attempt')
            db.session.add(audit_log)
            db.session.commit()
            return jsonify({"msg": "Account temporarily locked due to suspicious activity"}), 403
        return jsonify({"msg": "Bad username or password"}), 401

    user.last_login = datetime.utcnow()
    user.login_attempts = 0
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({"msg": "Bad username or password"}), 401

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    user.last_login = datetime.utcnow()
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=15))
    return jsonify(access_token=access_token)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from ..models import User, AuditLog, db
from werkzeug.security import check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    success = False
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        success = True
        response = jsonify(access_token=access_token, refresh_token=refresh_token)
    else:
        response = jsonify({"msg": "Bad username or password"}), 401

    audit_log = AuditLog(
        user_id=user.id if user else None,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        success=success
    )
    db.session.add(audit_log)
    db.session.commit()

    return response
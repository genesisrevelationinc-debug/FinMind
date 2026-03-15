from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.webhooks import webhook
from backend.app.models import User
from backend.app.extensions import jwt
from werkzeug.security import generate_password_hash, check_password_hash
        db.session.commit()
        access_token = jwt.create_access_token(identity=user.id)
        refresh_token = jwt.create_refresh_token(identity=user.id)
        webhook.send('user.created', user_id=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 201
    except Exception as e:
        db.session.rollback()
from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.webhooks import webhook
from backend.app.models import Bill
from backend.app.extensions import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
        db.session.commit()
        access_token = jwt.create_access_token(identity=current_user)
        refresh_token = jwt.create_refresh_token(identity=current_user)
        webhook.send('bill.created', bill_id=bill.id)
        return jsonify(bill=bill.to_dict()), 201
    except Exception as e:
        db.session.rollback()
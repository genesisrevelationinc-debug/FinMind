from flask import Blueprint, request, jsonify
from flask_webhook import emit_event
from backend.app.models import Bill, db

bp = Blueprint('bills', __name__, url_prefix='/bills')
    db.session.add(new_bill)
    db.session.commit()

    emit_event('bill_created', new_bill)
    return jsonify(new_bill.to_dict()), 201
from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import Reminder
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

bp = Blueprint('reminders', __name__, url_prefix='/reminders')

@bp.route('/run', methods=['POST'])
@jwt_required()
def run_reminders():
    current_user = get_jwt_identity()
    reminders = Reminder.query.filter_by(user_id=current_user, sent=False).all()
    for reminder in reminders:
        if reminder.due_date <= datetime.datetime.utcnow():
            # Logic to send reminder (e.g., email, SMS)
            reminder.sent = True
            db.session.commit()
    return jsonify({"message": "Reminders processed"}), 200
from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import Reminder
from ..extensions import scheduler

bp = Blueprint('reminders', __name__, url_prefix='/reminders')

@bp.route('/run', methods=['POST'])
def run_reminders():
    # Logic to manually trigger reminders
    app.logger.info('Manually running reminders...')
    # Logic to send reminders
    return jsonify({"message": "Reminders triggered"}), 200

@bp.route('/', methods=['GET'])
def get_reminders():
    reminders = Reminder.query.all()
    return jsonify([reminder.to_dict() for reminder in reminders])

@bp.route('/', methods=['POST'])
def create_reminder():
    data = request.get_json()
    reminder = Reminder(name=data['name'], due_date=data['due_date'], channel=data['channel'])
    db.session.add(reminder)
    db.session.commit()
    return jsonify(reminder.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_reminder(id):
    data = request.get_json()
    reminder = Reminder.query.get_or_404(id)
    reminder.name = data['name']
    reminder.due_date = data['due_date']
    reminder.channel = data['channel']
    db.session.commit()
    return jsonify(reminder.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted"}), 200
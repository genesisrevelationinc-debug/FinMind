from flask import Blueprint, jsonify, request
from ..extensions import scheduler, db
from ..models import Reminder

reminders = Blueprint('reminders', __name__, url_prefix='/reminders')

@reminders.route('/run', methods=['POST'])
def run_reminders():
    reminders = Reminder.query.all()
    for reminder in reminders:
        scheduler.add_job(
            func=send_reminder,
            trigger='date',
            run_date=reminder.due_date,
            id=str(reminder.id),
            name=reminder.name,
            replace_existing=True
        )
    return jsonify({"message": "Reminders scheduled"}), 200

def send_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        # Logic to send reminder via email or WhatsApp
        print(f"Sending reminder: {reminder.name}")
        # Mark reminder as sent or update status
        reminder.sent = True
        db.session.commit()
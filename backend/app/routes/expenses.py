from flask import Blueprint, request, jsonify
from flask_webhook import emit_event
from backend.app.models import Expense, db

bp = Blueprint('expenses', __name__, url_prefix='/expenses')
    db.session.add(new_expense)
    db.session.commit()

    emit_event('expense_created', new_expense)
    return jsonify(new_expense.to_dict()), 201
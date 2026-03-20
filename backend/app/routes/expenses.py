from flask import Blueprint, request, jsonify
from flask_webhook import emit_event
from backend.app.models import db, Expense
from backend.app.extensions import db

    db.session.add(new_expense)
    db.session.commit()

    emit_event('expense_created', new_expense)
    return jsonify(new_expense.to_dict()), 201
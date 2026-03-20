from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Expense, Bill
from datetime import datetime, timedelta

bp = Blueprint('insights', __name__, url_prefix='/insights')

@bp.route('/weekly', methods=['GET'])
@jwt_required()
def weekly_summary():
    user_id = get_jwt_identity()
    start_of_week = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday(), hours=datetime.utcnow().hour, minutes=datetime.utcnow().minute, seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)

    expenses = Expense.query.filter_by(user_id=user_id).filter(Expense.date >= start_of_week, Expense.date <= end_of_week).all()
    bills = Bill.query.filter_by(user_id=user_id).filter(Bill.due_date >= start_of_week, Bill.due_date <= end_of_week).all()

    total_expenses = sum(expense.amount for expense in expenses)
    total_bills = sum(bill.amount for bill in bills)

    summary = {
        'start_of_week': start_of_week.isoformat(),
        'end_of_week': end_of_week.isoformat(),
        'total_expenses': total_expenses,
        'total_bills': total_bills,
        'expenses': [{'id': expense.id, 'amount': expense.amount, 'category': expense.category, 'date': expense.date.isoformat()} for expense in expenses],
        'bills': [{'id': bill.id, 'name': bill.name, 'amount': bill.amount, 'due_date': bill.due_date.isoformat()} for bill in bills]
    }

    return jsonify(summary), 200
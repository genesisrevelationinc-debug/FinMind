from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Expense, Bill
from datetime import datetime, timedelta

bp = Blueprint('insights', __name__, url_prefix='/insights')

@bp.route('/weekly', methods=['GET'])
@jwt_required()
def weekly_summary():
    user_id = get_jwt_identity()
    start_date = datetime.utcnow() - timedelta(days=7)
    end_date = datetime.utcnow()

    expenses = Expense.query.filter_by(user_id=user_id).filter(Expense.date >= start_date, Expense.date <= end_date).all()
    bills = Bill.query.filter_by(user_id=user_id).filter(Bill.due_date >= start_date, Bill.due_date <= end_date).all()

    total_expenses = sum(expense.amount for expense in expenses)
    total_bills = sum(bill.amount for bill in bills)

    summary = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'total_expenses': total_expenses,
        'total_bills': total_bills,
        'expenses': [{'amount': exp.amount, 'category': exp.category, 'date': exp.date.isoformat()} for exp in expenses],
        'bills': [{'name': bill.name, 'amount': bill.amount, 'due_date': bill.due_date.isoformat()} for bill in bills]
    }

    return jsonify(summary), 200
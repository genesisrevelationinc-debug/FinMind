from flask import Blueprint, jsonify
from ..models import db, Expense, Bill
from datetime import datetime, timedelta

bp = Blueprint('insights', __name__)

@bp.route('/weekly', methods=['GET'])
def weekly_summary():
    current_date = datetime.utcnow()
    start_of_week = current_date - timedelta(days=current_date.weekday(), hours=current_date.hour, minutes=current_date.minute, seconds=current_date.second, microseconds=current_date.microsecond)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)

    expenses = Expense.query.filter(Expense.date >= start_of_week, Expense.date <= end_of_week).all()
    bills = Bill.query.filter(Bill.due_date >= start_of_week, Bill.due_date <= end_of_week).all()

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
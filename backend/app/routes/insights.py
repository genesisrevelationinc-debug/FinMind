from flask import Blueprint, jsonify
from ..extensions import db
from ..models import Expense, Bill
from datetime import datetime, timedelta

bp = Blueprint('insights', __name__, url_prefix='/insights')

@bp.route('/weekly', methods=['GET'])
def weekly_summary():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    expenses = Expense.query.filter(Expense.date >= start_date, Expense.date <= end_date).all()
    bills = Bill.query.filter(Bill.due_date >= start_date, Bill.due_date <= end_date).all()

    total_expenses = sum(expense.amount for expense in expenses)
    total_bills = sum(bill.amount for bill in bills)

    expense_categories = {}
    for expense in expenses:
        if expense.category in expense_categories:
            expense_categories[expense.category] += expense.amount
        else:
            expense_categories[expense.category] = expense.amount

    summary = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'total_expenses': total_expenses,
        'total_bills': total_bills,
        'expense_categories': expense_categories
    }

    return jsonify(summary)
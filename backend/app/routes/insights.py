from flask import Blueprint, jsonify
from ..models import db, Expense, Bill
from datetime import datetime, timedelta

bp = Blueprint('insights', __name__, url_prefix='/insights')

@bp.route('/weekly', methods=['GET'])
def weekly_summary():
    current_date = datetime.utcnow()
    start_of_week = current_date - timedelta(days=current_date.weekday(), weeks=1)
    end_of_week = start_of_week + timedelta(days=6)

    expenses = Expense.query.filter(
        Expense.date >= start_of_week,
        Expense.date <= end_of_week
    ).all()

    bills = Bill.query.filter(
        Bill.due_date >= start_of_week,
        Bill.due_date <= end_of_week
    ).all()

    total_expenses = sum(expense.amount for expense in expenses)
    total_bills = sum(bill.amount for bill in bills)

    summary = {
        "start_of_week": start_of_week.isoformat(),
        "end_of_week": end_of_week.isoformat(),
        "total_expenses": total_expenses,
        "total_bills": total_bills,
        "expenses": [{"id": exp.id, "amount": exp.amount, "category": exp.category, "date": exp.date.isoformat()} for exp in expenses],
        "bills": [{"id": bill.id, "name": bill.name, "amount": bill.amount, "due_date": bill.due_date.isoformat()} for bill in bills]
    }

    return jsonify(summary)
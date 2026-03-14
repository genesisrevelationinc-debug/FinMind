from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from ..models import db, Expense, Bill

insights_bp = Blueprint('insights', __name__)

@insights_bp.route('/weekly', methods=['GET'])
def weekly_summary():
    # Calculate the start and end of the current week
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query expenses for the current week
    weekly_expenses = Expense.query.filter(
        Expense.date >= start_of_week,
        Expense.date <= end_of_week
    ).all()

    # Query bills for the current week
    weekly_bills = Bill.query.filter(
        Bill.due_date >= start_of_week,
        Bill.due_date <= end_of_week
    ).all()

    # Calculate total expenses and bills
    total_expenses = sum(expense.amount for expense in weekly_expenses)
    total_bills = sum(bill.amount for bill in weekly_bills)

    # Generate summary
    summary = {
        "start_date": start_of_week.isoformat(),
        "end_date": end_of_week.isoformat(),
        "total_expenses": total_expenses,
        "total_bills": total_bills,
        "expenses": [{"id": exp.id, "amount": exp.amount, "category": exp.category, "date": exp.date.isoformat()} for exp in weekly_expenses],
        "bills": [{"id": bill.id, "amount": bill.amount, "name": bill.name, "due_date": bill.due_date.isoformat()} for bill in weekly_bills]
    }

    return jsonify(summary)

@insights_bp.route('/weekly/trends', methods=['GET'])
def weekly_trends():
    # Calculate the start and end of the current week
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query expenses for the current week
    weekly_expenses = Expense.query.filter(
        Expense.date >= start_of_week,
        Expense.date <= end_of_week
    ).all()

    # Calculate trends (e.g., highest expense category)
    category_totals = {}
    for expense in weekly_expenses:
        if expense.category in category_totals:
            category_totals[expense.category] += expense.amount
        else:
            category_totals[expense.category] = expense.amount

    # Generate trends summary
    trends = {
        "start_date": start_of_week.isoformat(),
        "end_date": end_of_week.isoformat(),
        "category_totals": category_totals
    }

    return jsonify(trends)
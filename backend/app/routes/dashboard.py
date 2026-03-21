from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User, Expense, Bill

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_financial_overview():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Fetch expenses and bills for the user
    expenses = Expense.query.filter_by(user_id=current_user_id).all()
    bills = Bill.query.filter_by(user_id=current_user_id).all()

    # Calculate total expenses and bills
    total_expenses = sum(expense.amount for expense in expenses)
    total_bills = sum(bill.amount for bill in bills)

    # Fetch categories for expenses
    categories = {expense.category for expense in expenses}
    category_breakdown = {category: sum(expense.amount for expense in expenses if expense.category == category) for category in categories}

    # Fetch upcoming bills
    upcoming_bills = [bill for bill in bills if not bill.paid]

    return jsonify({
        "total_expenses": total_expenses,
        "total_bills": total_bills,
        "category_breakdown": category_breakdown,
        "upcoming_bills": [{"id": bill.id, "name": bill.name, "amount": bill.amount, "due_date": bill.due_date} for bill in upcoming_bills]
    }), 200
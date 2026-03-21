from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, Expense, Bill
from sqlalchemy.orm import joinedload

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_financial_overview():
    current_user_id = get_jwt_identity()
    user = User.query.options(joinedload(User.expenses), joinedload(User.bills)).get(current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    total_expenses = sum(expense.amount for expense in user.expenses)
    total_bills = sum(bill.amount for bill in user.bills)
    upcoming_bills = [bill for bill in user.bills if not bill.paid]

    overview = {
        "total_expenses": total_expenses,
        "total_bills": total_bills,
        "upcoming_bills": [{
            "id": bill.id,
            "name": bill.name,
            "amount": bill.amount,
            "due_date": bill.due_date.isoformat(),
            "paid": bill.paid
        } for bill in upcoming_bills]
    }

    return jsonify(overview), 200
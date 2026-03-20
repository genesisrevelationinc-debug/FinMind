from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import User, Expense, Bill

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/overview', methods=['GET'])
def get_overview():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    expenses = Expense.query.filter_by(user_id=user_id).all()
    bills = Bill.query.filter_by(user_id=user_id).all()

    total_expenses = sum(expense.amount for expense in expenses)
    total_bills = sum(bill.amount for bill in bills)

    return jsonify({
        'user_id': user.id,
        'total_expenses': total_expenses,
        'total_bills': total_bills,
        'expenses': [{'id': exp.id, 'amount': exp.amount, 'category': exp.category, 'notes': exp.notes, 'date': exp.date} for exp in expenses],
        'bills': [{'id': bill.id, 'name': bill.name, 'amount': bill.amount, 'cadence': bill.cadence, 'due_date': bill.due_date, 'channel': bill.channel} for bill in bills]
    })
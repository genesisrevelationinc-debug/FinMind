from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, Expense, Bill
from ..extensions import cache

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_financial_overview():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Fetch cached data or compute if not available
    monthly_summary_key = f"user:{user_id}:monthly_summary:{request.args.get('month', 'current')}"
    monthly_summary = cache.get(monthly_summary_key)
    if not monthly_summary:
        monthly_summary = compute_monthly_summary(user_id, request.args.get('month', 'current'))
        cache.set(monthly_summary_key, monthly_summary, timeout=1800)  # 30 minutes

    upcoming_bills_key = f"user:{user_id}:upcoming_bills"
    upcoming_bills = cache.get(upcoming_bills_key)
    if not upcoming_bills:
        upcoming_bills = compute_upcoming_bills(user_id)
        cache.set(upcoming_bills_key, upcoming_bills, timeout=900)  # 15 minutes

    return jsonify({
        "monthly_summary": monthly_summary,
        "upcoming_bills": upcoming_bills
    })

def compute_monthly_summary(user_id, month):
    # Placeholder for actual computation logic
    return {"total_expenses": 1000, "categories": {"food": 200, "transport": 150}}

def compute_upcoming_bills(user_id):
    # Placeholder for actual computation logic
    return [{"name": "Rent", "amount": 1200, "due_date": "2023-10-01", "paid": False}]
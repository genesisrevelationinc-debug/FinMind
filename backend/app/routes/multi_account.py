from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User, Account

bp = Blueprint('multi_account', __name__, url_prefix='/multi-account')

@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_multi_account_overview():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    accounts = Account.query.filter_by(user_id=current_user_id).all()
    overview = []
    for account in accounts:
        account_overview = {
            "account_id": account.id,
            "balance": account.balance,
            "currency": account.currency,
            "transactions": [t.to_dict() for t in account.transactions]
        }
        overview.append(account_overview)
    return jsonify(overview), 200
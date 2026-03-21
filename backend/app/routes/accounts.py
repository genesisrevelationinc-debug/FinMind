from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Account

accounts_bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@accounts_bp.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=user_id).all()
    return jsonify([account.to_dict() for account in accounts]), 200

@accounts_bp.route('/', methods=['POST'])
@jwt_required()
def add_account():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_account = Account(user_id=user_id, name=data['name'], balance=data['balance'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify(new_account.to_dict()), 201

@accounts_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted'}), 200
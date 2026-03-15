from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import User, db
from ..extensions import audit_log
auth_bp = Blueprint('auth', __name__)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/export_data', methods=['GET'])
@jwt_required()
def export_data():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Export user data
    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "expenses": [expense.to_dict() for expense in user.expenses],
        "bills": [bill.to_dict() for bill in user.bills],
        "reminders": [reminder.to_dict() for reminder in user.reminders]
    }

    audit_log.info(f"User {user_id} exported their data.")
    return jsonify(user_data), 200


@auth_bp.route('/delete_data', methods=['DELETE'])
@jwt_required()
def delete_data():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Delete user data
    db.session.delete(user)
    db.session.commit()

    audit_log.info(f"User {user_id} permanently deleted their data.")
    return jsonify({"msg": "Data deleted successfully"}), 200

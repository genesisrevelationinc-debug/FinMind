from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import SavingsGoal, Milestone

bp = Blueprint('savings_goals', __name__)

@bp.route('/', methods=['POST'])
def create_savings_goal():
    data = request.get_json()
    new_goal = SavingsGoal(
        user_id=data['user_id'],
        name=data['name'],
        target_amount=data['target_amount'],
        description=data.get('description')
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({'id': new_goal.id}), 201

@bp.route('/<int:goal_id>/milestones', methods=['POST'])
def create_milestone(goal_id):
    data = request.get_json()
    new_milestone = Milestone(
        savings_goal_id=goal_id,
        name=data['name'],
        amount=data['amount'],
        description=data.get('description')
    )
    db.session.add(new_milestone)
    db.session.commit()
    return jsonify({'id': new_milestone.id}), 201

@bp.route('/<int:goal_id>', methods=['GET'])
def get_savings_goal(goal_id):
    goal = SavingsGoal.query.get_or_404(goal_id)
    return jsonify({
        'id': goal.id,
        'user_id': goal.user_id,
        'name': goal.name,
        'target_amount': goal.target_amount,
        'current_amount': goal.current_amount,
        'description': goal.description,
        'milestones': [{'id': m.id, 'name': m.name, 'amount': m.amount, 'description': m.description} for m in goal.milestones]
    })

@bp.route('/<int:goal_id>', methods=['PUT'])
def update_savings_goal(goal_id):
    data = request.get_json()
    goal = SavingsGoal.query.get_or_404(goal_id)
    goal.name = data.get('name', goal.name)
    goal.target_amount = data.get('target_amount', goal.target_amount)
    goal.description = data.get('description', goal.description)
    db.session.commit()
    return jsonify({'message': 'Savings goal updated successfully'})

@bp.route('/<int:goal_id>', methods=['DELETE'])
def delete_savings_goal(goal_id):
    goal = SavingsGoal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'message': 'Savings goal deleted successfully'})
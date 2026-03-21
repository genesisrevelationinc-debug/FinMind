from flask import Blueprint, request, jsonify
from ..models import db, SavingsGoal, Milestone
from ..extensions import jwt_required, get_jwt_identity

savings_goals_bp = Blueprint('savings_goals', __name__, url_prefix='/savings_goals')

@savings_goals_bp.route('/', methods=['POST'])
@jwt_required()
def create_savings_goal():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_goal = SavingsGoal(
        user_id=user_id,
        goal_name=data['goal_name'],
        target_amount=data['target_amount'],
        start_date=data.get('start_date'),
        end_date=data.get('end_date')
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({'message': 'Savings goal created successfully'}), 201

@savings_goals_bp.route('/<int:goal_id>/milestones', methods=['POST'])
@jwt_required()
def create_milestone(goal_id):
    data = request.get_json()
    new_milestone = Milestone(
        savings_goal_id=goal_id,
        milestone_name=data['milestone_name'],
        amount=data['amount']
    )
    db.session.add(new_milestone)
    db.session.commit()
    return jsonify({'message': 'Milestone created successfully'}), 201

@savings_goals_bp.route('/<int:goal_id>', methods=['GET'])
@jwt_required()
def get_savings_goal(goal_id):
    goal = SavingsGoal.query.get_or_404(goal_id)
    return jsonify({
        'id': goal.id,
        'goal_name': goal.goal_name,
        'target_amount': goal.target_amount,
        'current_amount': goal.current_amount,
        'start_date': goal.start_date.isoformat(),
        'end_date': goal.end_date.isoformat() if goal.end_date else None,
        'milestones': [{'id': m.id, 'milestone_name': m.milestone_name, 'amount': m.amount, 'achieved': m.achieved} for m in goal.milestones]
    })

@savings_goals_bp.route('/<int:goal_id>/milestones/<int:milestone_id>', methods=['PUT'])
@jwt_required()
def update_milestone(goal_id, milestone_id):
    data = request.get_json()
    milestone = Milestone.query.get_or_404(milestone_id)
    milestone.milestone_name = data.get('milestone_name', milestone.milestone_name)
    milestone.amount = data.get('amount', milestone.amount)
    milestone.achieved = data.get('achieved', milestone.achieved)
    db.session.commit()
    return jsonify({'message': 'Milestone updated successfully'})

@savings_goals_bp.route('/<int:goal_id>/milestones/<int:milestone_id>', methods=['DELETE'])
@jwt_required()
def delete_milestone(goal_id, milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    db.session.delete(milestone)
    db.session.commit()
    return jsonify({'message': 'Milestone deleted successfully'})
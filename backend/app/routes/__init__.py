from flask import Blueprint
from . import auth, expenses, bills, reminders, insights

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(auth.bp, url_prefix='/auth')
api_bp.register_blueprint(expenses.bp, url_prefix='/expenses')
api_bp.register_blueprint(bills.bp, url_prefix='/bills')
api_bp.register_blueprint(reminders.bp, url_prefix='/reminders')
api_bp.register_blueprint(insights.bp, url_prefix='/insights')
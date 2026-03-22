from flask import Blueprint
from . import auth
from . import savings
api_bp = Blueprint('api', __name__, url_prefix='/api')
api_bp.register_blueprint(expenses.bp)
api_bp.register_blueprint(bills.bp)
api_bp.register_blueprint(reminders.bp)
api_bp.register_blueprint(savings.bp)
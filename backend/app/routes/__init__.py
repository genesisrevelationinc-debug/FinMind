from flask import Blueprint
from . import auth
from . import savings
api = Blueprint('api', __name__)
api.register_blueprint(expenses.bp, url_prefix='/expenses')
api.register_blueprint(bills.bp, url_prefix='/bills')
api.register_blueprint(reminders.bp, url_prefix='/reminders')
api.register_blueprint(savings.bp, url_prefix='/savings')
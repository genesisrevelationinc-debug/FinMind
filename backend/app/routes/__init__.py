from flask import Blueprint
from . import multi_account
api_bp = Blueprint('api', __name__)
from . import expenses
from . import bills
from . import reminders
api_bp.register_blueprint(multi_account.bp, url_prefix='/multi-account')
from flask import Blueprint
from .auth import auth_bp
from .savings import savings_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(savings_bp, url_prefix='/savings')

from . import auth, savings
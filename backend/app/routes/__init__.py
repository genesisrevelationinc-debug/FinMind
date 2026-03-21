from flask import Blueprint
from . import auth
from . import savings
api = Blueprint('api', __name__)
api.register_blueprint(auth.bp)
api.register_blueprint(savings.bp)
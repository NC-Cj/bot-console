from flask import Blueprint

log_blue = Blueprint('log', __name__, url_prefix='/log')

from . import view

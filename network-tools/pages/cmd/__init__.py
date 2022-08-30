from flask import Blueprint

cmd_blue = Blueprint('cmd', __name__, url_prefix='/cmd')

from . import view

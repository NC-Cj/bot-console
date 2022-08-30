from flask import Blueprint

action_blue = Blueprint('actions', __name__, url_prefix='/actions')

from . import view
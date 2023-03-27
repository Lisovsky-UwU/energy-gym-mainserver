from flask import Blueprint


api = Blueprint('api', __name__)

from .available_time import avtime_bl
from .entry import entry_bl
from .user import user_bl

api.register_blueprint(avtime_bl, url_prefix='/avtime')
api.register_blueprint(entry_bl, url_prefix='/entry')
api.register_blueprint(user_bl, url_prefix='/user')


from . import handlers

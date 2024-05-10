from flask import Blueprint


api = Blueprint('api', __name__)

from .available_time import avtime_bl
from .report import report_bl
from .entry import entry_bl
from .visit import visit_bl
from .user import user_bl
from .news import new_bl
from .ads import ads_bl

api.register_blueprint(avtime_bl, url_prefix='/avtime')
api.register_blueprint(report_bl, url_prefix='/report')
api.register_blueprint(entry_bl, url_prefix='/entry')
api.register_blueprint(visit_bl, url_prefix='/visit')
api.register_blueprint(user_bl, url_prefix='/user')
api.register_blueprint(new_bl, url_prefix='/new')
api.register_blueprint(ads_bl, url_prefix='/gym-news')


from . import handlers

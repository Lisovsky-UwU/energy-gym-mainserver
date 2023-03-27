from flask import Blueprint

from ...controllers import ControllerFactory


avtime_bl = Blueprint('avtime', 'avtime')

@avtime_bl.get('/get-all')
def get_all_avtimes():
    return ControllerFactory.avtime().get_all().json()

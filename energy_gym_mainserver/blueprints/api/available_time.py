from flask import Blueprint

from ...controllers import ControllerFactory


avtime_bl = Blueprint('avtime', 'avtime')


@avtime_bl.post('/create')
def create_avtime():
    return {'result': 'in develop...'}


@avtime_bl.get('/get')
def get_avtimes():
    return ControllerFactory.avtime().get_all().dict()


@avtime_bl.put('/edit')
def edit_avtime():
    return {'result': 'in develop...'}


@avtime_bl.delete('/delete')
def delete_avtime():
    return {'result': 'in develop...'}

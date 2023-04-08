from flask import Blueprint
from flask import request

from .handlers import format_response
from ...models import dto
from ...controllers import ControllerFactory


avtime_bl = Blueprint('avtime', 'avtime')


@avtime_bl.post('/create')
@format_response
def create_avtime():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.avtime().create(
        dto.AvailableTimeAddRequest.parse_obj(avtime)
        for avtime in data
    )


@avtime_bl.get('/get')
@format_response
def get_avtimes():
    return ControllerFactory.avtime().get_all()


@avtime_bl.put('/edit')
@format_response
def edit_avtime():
    return {'result': 'in develop...'}


@avtime_bl.delete('/delete')
@format_response
def delete_avtime():
    return {'result': 'in develop...'}

from flask import Blueprint
from flask import request

from ...controllers import ControllerFactory
from ...models import dto
from ...exceptions import InvalidRequestException


entry_bl = Blueprint('entry', 'entry')

@entry_bl.get('/get-all')
def get_all_entries():
    return ControllerFactory.entry().get_all().dict()


@entry_bl.post('/get')
def get_entries():
    data = request.json
    controller = ControllerFactory.entry()

    if 'user' in data:
        return controller.get_for_user(data['user']).dict()
    elif 'avtime' in data:
        return controller.get_for_avtime(data['avtime']).dict()
    else:
        raise InvalidRequestException('Отсутствует аргумент user или avtime')


@entry_bl.post('/create')
def create_entries():
    return ControllerFactory.entry().create_for_list(
        dto.EntryList.parse_obj(request.json)
    ).dict()

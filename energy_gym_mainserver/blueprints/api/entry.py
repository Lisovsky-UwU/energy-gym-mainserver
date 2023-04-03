from flask import Blueprint
from flask import request

from ...controllers import ControllerFactory
from ...models import dto
from ...exceptions import InvalidRequestException


entry_bl = Blueprint('entry', 'entry')


@entry_bl.post('/create')
def create_entry():
    return {'result': 'in develop...'}


@entry_bl.post('/create-any')
def create_any_entry():
    return ControllerFactory.entry().create_for_list(
        dto.EntryList.parse_obj(request.json)
    ).dict()


@entry_bl.get('/get')
def get_entries():
    return {'result': 'in develop...'}


@entry_bl.get('/get-any')
def get_any_entries():
    try:
        data = request.get_json()
    except:
        raise InvalidRequestException('Тело запроса должно быть в формате JSON')
    
    controller = ControllerFactory.entry()

    if 'user' in data:
        return controller.get_for_user(data['user']).dict()
    elif 'avtime' in data:
        return controller.get_for_avtime(data['avtime']).dict()
    else:
        return ControllerFactory.entry().get_all().dict()


@entry_bl.delete('/delete')
def delete_entries():
    return {'result': 'in develop...'}


@entry_bl.delete('/delete-any')
def delete_any_entries():
    return {'result': 'in develop...'}

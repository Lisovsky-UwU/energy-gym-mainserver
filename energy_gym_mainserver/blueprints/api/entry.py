from flask import Blueprint
from flask import request

from ...controllers import ControllerFactory
from ...models import dto


entry_bl = Blueprint('entry', 'entry')


@entry_bl.post('/create')
def create_entry():
    return ControllerFactory.entry().create_by_user(
        int(request.headers.get('user-id')),
        request.get_json()
    ).dict()


@entry_bl.post('/create-any')
def create_any_entry():
    return ControllerFactory.entry().create_for_list(
        dto.EntryAddList(
            data = list(
                dto.EntryAddRequest.parse_obj(entry)
                for entry in request.get_json()
            )
        )
    ).dict()


@entry_bl.get('/get')
def get_entries():
    return ControllerFactory.entry().get_for_user(
        int(request.headers.get('user-id'))
    ).dict()


@entry_bl.get('/get-any')
def get_any_entries():
    controller = ControllerFactory.entry()
    try:
        data = request.get_json()
    except:
        return controller.get_all().dict()

    if 'user' in data:
        return controller.get_for_user(data['user']).dict()
    elif 'avtime' in data:
        return controller.get_for_avtime(data['avtime']).dict()
    else:
        return controller.get_all().dict()


@entry_bl.delete('/delete')
def delete_entries():
    return ControllerFactory.entry().delete_for_id_list(
        request.get_json(),
        int(request.headers.get('user-id'))
    ).dict()


@entry_bl.delete('/delete-any')
def delete_any_entries():
    return ControllerFactory.entry().delete_for_id_list(
        request.get_json(),
        int(request.headers.get('user-id')),
        True
    ).dict()

from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import ControllerFactory
from ...models import dto


entry_bl = Blueprint('entry', 'entry')


@entry_bl.post('/create')
@format_response
def create_entry():
    return ControllerFactory.entry().create_by_user(
        int(request.headers.get('user-id')),
        request.get_json()
    )


@entry_bl.post('/create-any')
@format_response
def create_any_entry():
    return ControllerFactory.entry().create_for_list(
        dto.EntryAddList(
            data = list(
                dto.EntryAddRequest.parse_obj(entry)
                for entry in request.get_json()
            )
        )
    )


@entry_bl.get('/get')
@format_response
def get_entries():
    return ControllerFactory.entry().get_for_user(
        int(request.headers.get('user-id'))
    )


@entry_bl.get('/get-any')
@format_response
def get_any_entries():
    controller = ControllerFactory.entry()
    try:
        data = request.get_json()
    except:
        return controller.get_all()

    if 'user' in data:
        return controller.get_for_user(data['user'])
    elif 'avtime' in data:
        return controller.get_for_avtime(data['avtime'])
    else:
        return controller.get_all()


@entry_bl.delete('/delete')
@format_response
def delete_entries():
    return ControllerFactory.entry().delete_for_id_list(
        request.get_json(),
        int(request.headers.get('user-id'))
    )


@entry_bl.delete('/delete-any')
@format_response
def delete_any_entries():
    return ControllerFactory.entry().delete_for_id_list(
        request.get_json(),
        int(request.headers.get('user-id')),
        True
    )

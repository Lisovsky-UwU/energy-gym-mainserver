from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import ControllerFactory
from ...controllers import EntryDBController
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
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.entry().create(
        dto.EntryAddRequest.parse_obj(entry)
        for entry in data
    )


@entry_bl.get('/check-open')
@format_response
def check_open():
    return EntryDBController.entry_is_open


@entry_bl.post('/change-open')
@format_response
def change_open():
    data = request.get_json()
    
    if isinstance(data, bool):
        EntryDBController.entry_is_open = data

    return EntryDBController.entry_is_open


@entry_bl.get('/get')
@format_response
def get_entries():
    return ControllerFactory.entry().get_for_user(
        int(request.headers.get('user-id'))
    )


@entry_bl.post('/get-any')
@format_response
def get_any_entries():
    controller = ControllerFactory.entry()
    try:
        data = request.get_json()
    except:
        return controller.get_any()

    return controller.get_any(**data)


@entry_bl.delete('/delete')
@format_response
def delete_entries():
    return ControllerFactory.entry().delete(
        request.get_json(),
        int(request.headers.get('user-id'))
    )


@entry_bl.delete('/delete-any')
@format_response
def delete_any_entries():
    return ControllerFactory.entry().delete(
        request.get_json(),
        int(request.headers.get('user-id')),
        True
    )

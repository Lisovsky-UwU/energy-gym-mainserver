from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import EntryDBController
from ...models import dto


entry_bl = Blueprint('entry', 'entry')


@entry_bl.post('/create')
@format_response
def create_entry():
    return EntryDBController().create_by_user(
        int(request.headers.get('user-id')),
        dto.EntryAddByUserRequest.parse_obj( request.json )
    )


@entry_bl.post('/create-any')
@format_response
def create_any_entry():
    return EntryDBController().create(
        dto.EntryAddRequest.parse_obj( request.json )
    )


@entry_bl.get('/check-open')
@format_response
def check_open():
    return dto.OpenEntryResponse(
        status=EntryDBController.entry_is_open()
    )


@entry_bl.post('/change-open')
@format_response
def change_open():
    data = dto.OpenEntryResponse.parse_obj( request.json )
    return dto.OpenEntryResponse(
        status=EntryDBController.change_entry_open(data.status)
    )
    


@entry_bl.get('/get')
@format_response
def get_entries():
    return EntryDBController().get_for_user(
        int(request.headers.get('user-id')),
        request.json.get('month')
    )


@entry_bl.post('/get-any')
@format_response
def get_any_entries():
    return EntryDBController().get(
        request.json.get('weekday'),
        request.json.get('deleted', False)
    )


@entry_bl.delete('/delete')
@format_response
def delete_entries():
    EntryDBController().delete(
        dto.DeleteRequest.parse_obj( request.json ).id,
        int(request.headers.get('user-id'))
    )
    return dto.SuccessResponse()


@entry_bl.delete('/delete-any')
@format_response
def delete_any_entries():
    EntryDBController().delete(
        dto.DeleteRequest.parse_obj( request.json ).id,
        int(request.headers.get('user-id')),
        True
    )
    return dto.SuccessResponse()

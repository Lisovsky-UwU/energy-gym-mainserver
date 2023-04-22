from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import ControllerFactory
from ...models import dto


user_bl = Blueprint('user', 'user')


@user_bl.post('/create')
@format_response
def create_user():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.user().create(
        dto.UserCreateRequest.parse_obj(user)
        for user in data
    )


@user_bl.get('/get')
@format_response
def get_user():
    return ControllerFactory.user().get(
        int(request.headers.get('user-id'))
    )


@user_bl.post('/get-any')
@format_response
def get_any_users():
    controller = ControllerFactory.user()
    try:
        data = request.get_json()
    except:
        return controller.get_any()

    return controller.get_any(**data)


@user_bl.put('/edit')
@format_response
def edit_entries():
    return ControllerFactory.user().user_data_update(
        int(request.headers.get('user-id')),
        dto.UserDataUpdateRequest.parse_obj(request.get_json())
    )


@user_bl.put('/edit-password')
@format_response
def edit_password():
    return ControllerFactory.user().user_password_update(
        int(request.headers.get('user-id')),
        dto.UserPasswordUpdateRequest.parse_obj(request.get_json())
    )


@user_bl.put('/edit-any')
@format_response
def edit_any_entries():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.user().update(
        dto.UserAnyDataUpdateRequest(**user)
        for user in data
    )


@user_bl.delete('/delete-any')
@format_response
def delete_any_entries():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.user().delete(data)

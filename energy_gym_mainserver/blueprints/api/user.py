from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import ControllerFactory
from ...models import dto


user_bl = Blueprint('user', 'user')


@user_bl.post('/create')
@format_response
def create_user():
    return ControllerFactory.user().create(
        dto.UserCreateRequest.parse_obj(request.get_json())
    )


@user_bl.get('/get')
@format_response
def get_user():
    return ControllerFactory.user().get(
        int(request.headers.get('user-id'))
    )


@user_bl.get('/get-any')
@format_response
def get_any_users():
    controller = ControllerFactory.user()
    try:
        data = request.get_json()
    except:
        return controller.get_all()

    if 'user' in data:
        return controller.get(data['user'])
    else:
        return controller.get_all()


@user_bl.put('/edit')
@format_response
def edit_entries():
    return ControllerFactory.user().user_data_update(
        int(request.headers.get('user-id')),
        dto.UserDataUpdateRequest.parse_obj(request.get_json())
    )


@user_bl.put('/edit-any')
@format_response
def edit_any_entries():
    return ControllerFactory.user().update_any_user_data(
        [ 
            dto.UserAnyDataUpdateRequest(**data)
            for data in request.get_json()
        ]
    )


@user_bl.delete('/delete-any')
@format_response
def delete_any_entries():
    return ControllerFactory.user().delete_for_id_list(
        request.get_json()
    )

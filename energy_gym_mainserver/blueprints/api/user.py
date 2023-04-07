from flask import Blueprint
from flask import request

from ...controllers import ControllerFactory
from ...models import dto


user_bl = Blueprint('user', 'user')


@user_bl.post('/create')
def create_user():
    return ControllerFactory.user().create(
        dto.UserCreateRequest.parse_obj(request.get_json())
    ).dict()


@user_bl.get('/get')
def get_user():
    return ControllerFactory.user().get(
        int(request.headers.get('user-id'))
    ).dict()


@user_bl.get('/get-any')
def get_any_users():
    controller = ControllerFactory.user()
    try:
        data = request.get_json()
    except:
        return controller.get_all().dict()

    if 'user' in data:
        return controller.get(data['user']).dict()
    else:
        return controller.get_all().dict()


@user_bl.put('/edit')
def edit_entries():
    return ControllerFactory.user().user_data_update(
        int(request.headers.get('user-id')),
        dto.UserDataUpdateRequest.parse_obj(request.get_json())
    ).dict()


@user_bl.put('/edit-any')
def edit_any_entries():
    return ControllerFactory.user().update_any_user_data(
        [ 
            dto.UserAnyDataUpdateRequest(**data)
            for data in request.get_json()
        ]
    ).dict()


@user_bl.delete('/delete-any')
def delete_any_entries():
    return ControllerFactory.user().delete_for_id_list(
        request.get_json()
    ).dict()

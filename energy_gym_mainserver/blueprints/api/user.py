from flask import Blueprint
from flask import request

from ...controllers import ControllerFactory
from ...models import dto
from ...exceptions import InvalidRequestException


user_bl = Blueprint('user', 'user')


@user_bl.post('/create')
def create_user():
    try:
        data = request.get_json()
    except:
        raise InvalidRequestException('Тело запроса должно быть в формате JSON')

    return ControllerFactory.user().create(
        dto.UserCreateRequest.parse_obj(data)
    ).dict()


@user_bl.get('/get')
def get_user():
    return {'result': 'in develop...'}


@user_bl.get('/get-any')
def get_any_users():
    return ControllerFactory.user().get_all().dict()


@user_bl.put('/edit')
def edit_entries():
    return {'result': 'in develop...'}


@user_bl.put('/edit-any')
def edit_any_entries():
    return {'result': 'in develop...'}


@user_bl.delete('/delete')
def delete_entries():
    return {'result': 'in develop...'}


@user_bl.delete('/delete-any')
def delete_any_entries():
    return {'result': 'in develop...'}

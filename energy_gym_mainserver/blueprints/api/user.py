from flask import Blueprint
from flask import request

from ...controllers import ControllerFactory
from ...models import dto


user_bl = Blueprint('user', 'user')

@user_bl.get('/get-all')
def get_all_users():
    return ControllerFactory.user().get_all().dict()


@user_bl.post('/create')
def create_user():
    return ControllerFactory.user().create(
        dto.UserCreateRequest.parse_obj(request.json)
    ).dict()

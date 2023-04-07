from flask import Blueprint
from flask import request

from ...controllers import ControllerFactory
from ...models import dto


ads_bl = Blueprint('asd', 'ads')


@ads_bl.post('/create')
def create_ads():
    return ControllerFactory.ads().create(
        int(request.headers.get('user-id')),
        request.get_json()
    ).dict()


@ads_bl.get('/get')
def get_ads():
    return ControllerFactory.ads().get_all().dict()


@ads_bl.put('/edit')
def edit_ads():
    return ControllerFactory.ads().update(
        dto.AdsUpdateRequest.parse_obj(request.get_json())
    ).dict()


@ads_bl.delete('/delete')
def delete_ads():
    return ControllerFactory.ads().delete_for_id_list(
        request.get_json()
    ).dict()

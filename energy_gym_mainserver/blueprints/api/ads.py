from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import ControllerFactory
from ...models import dto


ads_bl = Blueprint('asd', 'ads')


@ads_bl.post('/create')
@format_response
def create_ads():
    return ControllerFactory.ads().create(
        int(request.headers.get('user-id')),
        request.get_json()
    )


@ads_bl.get('/get')
@format_response
def get_ads():
    return ControllerFactory.ads().get_all()


@ads_bl.put('/edit')
@format_response
def edit_ads():
    return ControllerFactory.ads().update(
        dto.AdsUpdateRequest.parse_obj(request.get_json())
    )


@ads_bl.delete('/delete')
@format_response
def delete_ads():
    return ControllerFactory.ads().delete_for_id_list(
        request.get_json()
    )

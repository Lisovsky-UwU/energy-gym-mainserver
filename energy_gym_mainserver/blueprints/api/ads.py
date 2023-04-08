from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import ControllerFactory
from ...models import dto


ads_bl = Blueprint('asd', 'ads')


@ads_bl.post('/create')
@format_response
def create_ads():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.ads().create(
        int(request.headers.get('user-id')),
        data
    )


@ads_bl.get('/get')
@format_response
def get_ads():
    return ControllerFactory.ads().get_all()


@ads_bl.post('/get-any')
@format_response
def get_any_ads():
    controller = ControllerFactory.ads()
    try:
        data = request.get_json()
    except:
        return controller.get_any()

    return controller.get_any(**data)


@ads_bl.put('/edit')
@format_response
def edit_ads():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.ads().update(
        dto.AdsUpdateRequest.parse_obj(ads)
        for ads in data
    )


@ads_bl.delete('/delete')
@format_response
def delete_ads():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.ads().delete(data)

from flask import Blueprint
from flask import request

from .handlers import format_response
from ...controllers import ControllerFactory
from ...models import dto


visit_bl = Blueprint('visit', 'visit')


@visit_bl.post('/create')
@format_response
def create_visit():
    data = request.get_json()
    if not isinstance(data, list):
        data = [data]

    return ControllerFactory.visit().create(
        dto.VisitCreateRequest.parse_obj(visit)
        for visit in data
    )


@visit_bl.get('/get')
@format_response
def get_visit():
    return { 'result': 'in develop...' }


@visit_bl.post('/get-any')
@format_response
def get_any_visits():
    controller = ControllerFactory.visit()
    try:
        data = request.get_json()
    except:
        return controller.get_any()

    return controller.get_any(**data)


@visit_bl.put('/edit')
@format_response
def edit_visits():
    return { 'result': 'in develop...' }

import json
import flask

from . import api
from ...exceptions import InvalidRequestException


@api.after_request
def response_format(response: flask.Response):
    body = response.json
    if not (isinstance(body, dict) and body.get('error', False)):
        response.data = json.dumps({'error': False, 'data': body})
    return response


@api.before_request
def json_chek():
    if flask.request.data and not flask.request.is_json:
        raise InvalidRequestException('Тело запроса должно быть в формате JSON')


@api.errorhandler(Exception)
def error_handle(error: Exception) -> flask.Response:
    response = flask.jsonify(
        {
            'error': True,
            'error_type': type(error).__name__,
            'error_message': str(error)
        }
    )
    return response, error.status_code if hasattr(error, 'status_code') else 500 # type: ignore

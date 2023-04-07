import json
import flask
from functools import wraps
from pydantic import BaseModel

from . import api
from ...exceptions import TokenException
from ...exceptions import InvalidRequestException
from ...configmodule import config


def format_response(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        return flask.jsonify(func(*args, **kwargs))
    
    return decorator


@api.after_request
def response_format_handler(response: flask.Response):
    body = response.json
    if not (isinstance(body, dict) and body.get('error', False)):
        response.data = json.dumps({'error': False, 'data': body})
    return response


@api.before_request
def json_chek():
    token = flask.request.headers.get('Token')
    if token is None:
        raise TokenException('Отсутствует токен в заголовке запроса')
    if token != config.common.token:
        raise TokenException('Неверный токен')

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

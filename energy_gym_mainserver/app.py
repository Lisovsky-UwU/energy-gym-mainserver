from flask.json.provider import DefaultJSONProvider
from flask import Flask
from loguru import logger
from waitress import serve
from flask_cors import CORS

from .configmodule import config
from .blueprints import api_bl


def build_app() -> Flask:
    logger.info('Сборка сервера')
    app = Flask(__name__)

    logger.info('Регистрация шаблонов')
    app.register_blueprint(api_bl, url_prefix='/api/v1')

    class JSONEncoder(DefaultJSONProvider):
        def __init__(self, app):
            super().__init__(app)

        def default(self, obj):
            if hasattr(obj, 'dict'):
                return obj.dict()
            else:
                return super().default(obj)

    app.json = JSONEncoder(app)

    if config.common.use_dev:
        logger.debug('Используется окружение разработки')
        CORS(app, allow_origin='*')

    return app


def run_app(app: Flask):
    logger.info('Запуск сервера')
    serve(app, listen=config.local_server.address, threads=config.local_server.threads)

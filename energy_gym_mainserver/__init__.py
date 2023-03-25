from loguru import logger

from .log import init_logger
from .app import build_app
from .configmodule import config


def start():
    init_logger()
    try:
        logger.info('Сборка сервера')
        app = build_app()
        logger.info('Запуск сервера')
        app.run(
            host=config.local_server.host,
            port=config.local_server.port,
            use_reloader=False
        )
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    start()

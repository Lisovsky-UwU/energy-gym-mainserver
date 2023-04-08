from loguru import logger

from .log import init_logger
from .app import build_app
from .managers import AvailableTimeCreatorManager
from .managers import EntryCreateOpeningManager
from .managers import VisitCreatorManager
from .controllers import ControllerFactory
from .controllers import EntryDBController
from .configmodule import config


def start():
    init_logger()
    try:
        logger.info('Запуск AvailableTimeCreatorManager')
        av_time_creator_manager = AvailableTimeCreatorManager(
            ControllerFactory.avtime()
        )
        av_time_creator_manager.start()
        logger.success('AvailableTimeCreatorManager запущен')

        logger.info('Запуск EntryCreateOpeningManager')
        entry_create_opening_manager = EntryCreateOpeningManager(
            EntryDBController
        )
        entry_create_opening_manager.start()
        logger.success('EntryCreateOpeningManager запущен')

        logger.info('Запуск VisitCreatorManager')
        visit_creator_manager = VisitCreatorManager(
            ControllerFactory.visit(),
            ControllerFactory.entry(),
            ControllerFactory.avtime()
        )
        visit_creator_manager.start()
        logger.success('VisitCreatorManager запущен')

        logger.info('Сборка сервера')
        app = build_app()
        logger.info('Запуск сервера')
        app.run(
            host=config.local_server.host,
            port=config.local_server.port,
            use_reloader=False
        )
    except KeyboardInterrupt:
        av_time_creator_manager.join()
        entry_create_opening_manager.join()
        visit_creator_manager.join()


if __name__ == '__main__':
    start()

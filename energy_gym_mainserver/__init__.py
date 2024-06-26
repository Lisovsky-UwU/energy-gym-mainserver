from loguru import logger

from .log import init_logger
from .app import build_app, run_app
from .managers import AvailableTimeCreatorManager, EntryCreateOpeningManager, VisitCreatorManager


def start():
    init_logger()
    try:
        logger.info('Запуск AvailableTimeCreatorManager')
        av_time_creator_manager = AvailableTimeCreatorManager()
        av_time_creator_manager.start()
        logger.success('AvailableTimeCreatorManager запущен')

        logger.info('Запуск EntryCreateOpeningManager')
        entry_create_opening_manager = EntryCreateOpeningManager()
        entry_create_opening_manager.start()
        logger.success('EntryCreateOpeningManager запущен')

        logger.info('Запуск VisitCreatorManager')
        visit_creator_manager = VisitCreatorManager()
        visit_creator_manager.start()
        logger.success('VisitCreatorManager запущен')

        run_app(build_app())
    except KeyboardInterrupt:
        av_time_creator_manager.join()
        entry_create_opening_manager.join()
        visit_creator_manager.join()


if __name__ == '__main__':
    start()

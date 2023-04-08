from threading import Thread
from datetime import date
from loguru import logger
from time import sleep

from ..configmodule import config
from ..controllers import AvailableTimeDBController
from ..controllers import EntryDBController
from ..controllers import VisitDBController
from ..models import dto
from ..utils import get_current_month


class VisitCreatorManager(Thread):

    def __init__(
        self, 
        visit_controller: VisitDBController, 
        entry_controller: EntryDBController,
        avtime_controller: AvailableTimeDBController
    ):
        super().__init__(daemon=True)
        self.__alive__ = True
        self.visit_controller = visit_controller
        self.entry_controller = entry_controller
        self.avtime_controller = avtime_controller
        self.name = 'VisitCreator-Manager'


    def run(self):
        while self.__alive__:
            logger.trace(f'{self.name} awaken')

            logger.debug('Проверка созданных отметок на текущий день')
            cur_date = date.today()
            avtime_list = list(
                avtime.id 
                for avtime in self.avtime_controller.get_any(get_current_month())
                if avtime.weekday == cur_date.weekday()
            )

            if len(self.visit_controller.get_any(av_times = avtime_list)) == 0:
                entry_list = self.entry_controller.get_any(av_times = avtime_list)
                if len(entry_list) > 0:
                    logger.info('Отсутствуют отметки на текущий день, создаем...')
                    self.visit_controller.create(
                        dto.VisitCreateRequest(
                            date  = cur_date,
                            entry = entry.id
                        )
                        for entry in entry_list
                    )
                    logger.success('Отметки на текущий день успешно созданы')


            logger.trace(f'{self.name} going sleep. zzzzz....')
            sleep(60 * config.common.visit_manager_timeout)


    def join(self, timeout = None) -> None:
        self.__alive__ = False
        return super().join(timeout)

from threading import Thread
from datetime import date
from loguru import logger
from typing import List
from time import sleep

from ..controllers import AvailableTimeDBController
from ..configmodule import config
from ..models import dto


class AvailableTimeCreatorManager(Thread):

    def __init__(self, avtime_controller: AvailableTimeDBController):
        super().__init__(daemon=True)
        self.__alive__ = True
        self.avtime_controller = avtime_controller
        self.name = 'AvailableTimeCreator-Manager'


    def run(self):
        while self.__alive__:
            logger.trace(f'{self.name} awaken')

            cur_date = date.today()
            if cur_date.day >= config.available_time.day_create:
                logger.debug('Проверка созданных записей на следующий месяц')
                try:
                    next_month = cur_date.replace(cur_date.year, cur_date.month + 1, 1) \
                        .strftime(config.available_time.month_format)
                except ValueError:
                    next_month = cur_date.replace(cur_date.year + 1, 1, 1) \
                        .strftime(config.available_time.month_format)

                avtimes_db = self.avtime_controller.get_any(
                    months  = next_month,
                    deleted = True
                )

                if len(avtimes_db) == 0: # 6 дней * 4 времени в день = 24 времени на месяц
                    logger.info('Создание времен на следующий месяц')
                    self.avtime_controller.create(
                        self.get_avtimes_add(next_month)
                    )
                    logger.success('Были созданы времена на следующий месяц')

            logger.trace(f'{self.name} going sleep. zzzzz....')
            sleep(60 * 10)


    def get_avtimes_add(self, month: str) -> List[dto.AvailableTimeAddRequest]:
        '''
        Здесь происходит генерация моделей на создания времени для записи
        по захардкоженным данным
        '''

        result_list = list()
        time_list = [ '16:00', '17:30', '19:00', '20:30' ]
        for weekday in range(6):
            result_list.extend(
                dto.AvailableTimeAddRequest(
                    weekday           = weekday,
                    time              = time,
                    number_of_persons = config.available_time.persons_numb,
                    month             = month
                )
                for time in time_list
            )
        
        return result_list


    def join(self, timeout = None) -> None:
        self.__alive__ = False
        return super().join(timeout)

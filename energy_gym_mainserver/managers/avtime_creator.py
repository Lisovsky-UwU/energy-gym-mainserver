from threading import Thread
from datetime import date
from loguru import logger
from typing import List
from time import sleep
from sqlalchemy import and_

from ..orm import SessionCtx, AvailableTime
from ..configmodule import config
from ..utils import get_next_month


class AvailableTimeCreatorManager(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.__alive__ = True
        self.name = 'AvailableTimeCreator-Manager'


    def run(self):
        while self.__alive__:
            logger.trace(f'{self.name} awaken')

            cur_date = date.today()
            if cur_date.day >= config.available_time.day_create:
                logger.debug('Проверка созданных времен для записи на следующий месяц')
                next_month = get_next_month()

                with SessionCtx() as session:
                    avtimes_db = session.query(AvailableTime).where(
                        and_(
                            AvailableTime.month == next_month,
                            AvailableTime.deleted == False
                        )
                    ).all()

                    if len(avtimes_db) == 0: # 6 дней * 4 времени в день = 24 времени на месяц
                        logger.info('Создание времен на следующий месяц')
                        session.add_all(
                            self.get_avtimes_add(next_month)
                        )
                        logger.success('Были созданы времена на следующий месяц')
                    
                    session.commit()

            logger.trace(f'{self.name} going sleep. zzzzz....')
            sleep(60 * 10)


    def get_avtimes_add(self, month: str) -> List[AvailableTime]:
        '''
        Здесь происходит генерация моделей на создания времени для записи
        по захардкоженным данным
        '''

        result_list = list()
        time_list = [ '16:00', '17:30', '19:00', '20:30' ]
        for weekday in range(6):
            result_list.extend(
                AvailableTime(
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

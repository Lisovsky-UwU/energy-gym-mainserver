import calendar
from threading import Thread
from datetime import datetime
from loguru import logger
from time import sleep

from ..controllers import EntryDBController
from ..configmodule import config


class EntryCreateOpeningManager(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.__alive__ = True
        self.name = 'EntryCreateOpening-Manager'


    def run(self):
        while self.__alive__:
            logger.trace(f'{self.name} awaken')

            cur_time = datetime.now()
            open_time = cur_time.strptime(config.available_time.opening_time, '%H:%M:%S %d') \
                        .replace(year = cur_time.year, month = cur_time.month)
            close_time = cur_time.replace(
                day    = calendar.monthrange(year = cur_time.year, month = cur_time.month)[1],
                hour   = 0,
                minute = 0,
                second = 0
            )
            
            if cur_time >= open_time and cur_time <= close_time:
                EntryDBController.change_entry_open(True)
                sleep_time = (close_time - cur_time).total_seconds()

            else:
                EntryDBController.change_entry_open(False)
                sleep_time = (self.get_next_time(config.available_time.opening_time) - cur_time).total_seconds()

            logger.debug(f'{self.name} going sleep for {round(sleep_time, 2)} seconds. zzzzz....')
            sleep(sleep_time)


    def get_next_time(self, str_time: str) -> datetime:
        cur_time = datetime.now()
        result = cur_time.strptime(str_time, '%H:%M:%S %d').replace(year = cur_time.year, month = cur_time.month)
        if (result - cur_time).total_seconds() < 0:
            try:
                result = result.replace(month=result.month + 1)
            except ValueError:
                result = result.replace(month=1, year=result.year + 1)
        
        return result


    def join(self, timeout = None) -> None:
        self.__alive__ = False
        return super().join(timeout)

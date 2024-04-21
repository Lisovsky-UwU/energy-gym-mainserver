from threading import Thread
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from loguru import logger
from time import sleep

from ..orm import SessionCtx, AvailableTime, Entry, Visit
from ..configmodule import config
from ..utils import get_current_month


class VisitCreatorManager(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.__alive__ = True
        self.name = 'VisitCreator-Manager'


    def create_for_date(self, month: str, created_date: date, session: Session):
        session.add_all(
            Visit(
                date  = created_date,
                entry = entry.id,
            )
            for entry in session.query(Entry).where(
                and_(
                    AvailableTime.month == month,
                    AvailableTime.weekday == created_date.weekday()
                )
            ).join(Entry.available_time).all()
        )
        logger.success(f'Созданы отметки посещений на день {created_date.strftime(config.common.date_format)}')


    def create_if_not_exists(self, month: str, created_date: date, session: Session):
        count = session.query(Visit).where(
            and_(
                AvailableTime.month == month,
                AvailableTime.weekday == created_date.weekday()
            )
        ) \
            .join(Visit.entry_model) \
            .join(Entry.available_time) \
            .count()
        
        if count == 0:
            logger.info(f'Отсутствуют отметки на {created_date.strftime(config.common.date_format)} день месяца, создаем')
            self.create_for_date(month, created_date, session)


    def create_for_prev_days(self):
        now = datetime.now()
        current_month = get_current_month()

        with SessionCtx() as session:
            for day in range(1, now.day):
                logger.debug(f'Проверка созданных отметок на {now.day} день месяца')
                created_date = date(now.year, now.month, day)

                # На воскресенье записи нет, так что скипаем
                if created_date.weekday() == 6:
                    continue

                self.create_if_not_exists(current_month, created_date, session)
            
            session.commit()
            logger.success('Созданные отметки успешно сохранены в БД')


    def run(self):
        self.create_for_prev_days()

        while self.__alive__:
            logger.trace(f'{self.name} awaken')

            with SessionCtx() as session:
                self.create_if_not_exists(
                    get_current_month(), 
                    datetime.now().date(), 
                    session
                )
                session.commit()
                logger.success('Созданные отметки успешно сохранены в БД')

            now = datetime.now()

            # В какое время проснется поток и будет создавать новые записи
            next_day = (now + timedelta(days=1)).replace(
                hour=1,
                minute=0,
                second=0,
                microsecond=0
            )
            delta = round((next_day - now).total_seconds())

            logger.trace(f'{self.name} going sleep to next day ({delta} seconds). zzzzz....')
            sleep(delta)


    def join(self, timeout = None) -> None:
        self.__alive__ = False
        return super().join(timeout)

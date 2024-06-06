from threading import Thread
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from loguru import logger
from time import sleep

from ..orm import SessionCtx, AvailableTime, Entry, Visit, User
from ..configmodule import config
from ..utils import get_current_month, get_next_month
from ..models import UserRole


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
                    AvailableTime.weekday == created_date.weekday(),
                    Entry.deleted == False
                )
            ).join(Entry.available_time).all()
        )
        logger.success(f'Созданы отметки посещений на день {created_date.strftime(config.common.date_format)}')


    def create_if_not_exists(self, month: str, created_date: date, session: Session):
        count = session.query(Visit).where(
            and_(
                Visit.date == created_date,
                Visit.deleted == False
            )
        ) \
            .join(Visit.entry_model) \
            .join(Entry.available_time) \
            .count()
        
        if count == 0:
            logger.info(f'Отсутствуют отметки на {created_date.strftime(config.common.date_format)}, создаем')
            self.create_for_date(month, created_date, session)
        else:
            logger.info(f'Отметки на {created_date.strftime(config.common.date_format)} уже существуют')


    def create_for_prev_days(self):
        now = datetime.now()
        current_month = get_current_month()

        with SessionCtx() as session:
            for day in range(1, now.day):
                created_date = date(now.year, now.month, day)
                # На воскресенье записи нет, так что скипаем
                if created_date.weekday() == 6:
                    logger.trace(f'Пропущен {created_date.strftime(config.common.date_format)} т.к. это воскресенье')
                    continue

                logger.debug(f'Проверка созданных отметок на {created_date.strftime(config.common.date_format)}')

                self.create_if_not_exists(current_month, created_date, session)
            
            session.commit()
            logger.success('Созданные отметки успешно сохранены в БД')


    def check_blocked_users(self, session: Session):
        blocked_users = session.query(User) \
            .where(
                and_(
                    User.role == UserRole.BLOCKED, 
                    User.deleted == False
                )
            ).all()

        for user in blocked_users:
            skiped_marks = session.query(Visit) \
                .where(
                    and_(
                        Entry.user == user.id,
                        Visit.mark == 0,
                        Visit.deleted == False,
                        AvailableTime.month == get_current_month()
                    )
                ) \
                .join(Visit.entry_model) \
                .join(Entry.available_time) \
                .count()
            if skiped_marks < config.common.max_skiped_visit:
                logger.success(f'Пользователь id={user.id} разблокирован')
                user.role = UserRole.STUDENT
            else:
                logger.info(f'Пользователь id={user.id} остается заблокированным')


    def check_visits(self, session: Session):
        t = (
            session.query(
                Entry.user,
                func.count('*').label('count')
            ).select_from(Visit)
            .join(Visit.entry_model)
            .join(Entry.available_time)
            .where(
                and_(
                    Visit.mark == 0,
                    Visit.deleted == False,
                    AvailableTime.month == get_current_month(),
                )
            )
            .group_by(Entry.user)
            .subquery('t')
        )

        users = (
            session.query(User)
            .where(
                and_(
                    User.role == UserRole.STUDENT,
                    User.deleted == False,
                    t.c.get('user') == User.id,
                    t.c.get('count') >= config.common.max_skiped_visit
                )
            )
            .join(Visit.entry_model)
            .join(Entry.available_time)
            .join(Entry.user_model)
            .all()
        )
        
        if len(users) == 0:
            logger.success('Отсутствуют пользователи для блокировки')

        for user in users:
            logger.debug(f'Пользователь с id={user.id} не явился на занятие больше {config.common.max_skiped_visit} раз. Удаляем его записи на следующий месяц и блокируем его.')
            user.role = UserRole.BLOCKED
            entries = (
                session.query(Entry)
                .join(Entry.available_time)
                .where(
                    and_(
                        Entry.user == user.id,
                        Entry.deleted == False,
                        AvailableTime.month == get_next_month(),
                    )
                )
                .all()
            )
            if len(entries) > 0:
                for entry in entries:
                    entry.deleted = True
                logger.success(f'Удалены записи пользователя id={user.id} на следующий месяц')
            else:
                logger.info(f'Пользователь с id={user.id} не имеет записи на следующий месяц')
            
            logger.success(f'По количество пропусков заблокирован пользователь id={user.id}')


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

                logger.info('Проверка заблокированных пользователей')
                self.check_blocked_users(session)
                session.commit()
                logger.success('Заблокированные пользователи успешно проверены')

                logger.info('Проверка еще не заблокированных пользователей')
                self.check_visits(session)
                session.commit()
                logger.success('Успешно проверены все посещения пользователей')

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

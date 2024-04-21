from typing import List
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..configmodule import config
from ..exceptions import LogicError, DataBaseException
from ..models import dto
from ..utils import get_next_month, get_current_month
from ..orm import Entry, SessionCtx, AvailableTime


class EntryDBController:

    _entry_is_open = False


    @classmethod
    def entry_is_open(cls) -> bool:
        return cls._entry_is_open


    @classmethod
    def change_entry_open(cls, status: bool) -> bool:
        cls._entry_is_open = status
        if cls._entry_is_open: 
            logger.success('Запись открыта')
        else: 
            logger.success('Запись закрыта')

        return cls.entry_is_open()

    def delete_old_entities(self, session: Session, user_id: int):
        old_entries = session.query(Entry).where(
            and_(
                Entry.user == user_id,
                Entry.deleted == False,
                AvailableTime.month == get_next_month()
            )
        ).join(Entry.available_time).all()
        for old_entry in old_entries:
            old_entry.deleted = True


    def create_by_user(self, user_id: int, data: dto.EntryAddByUserRequest) -> List[dto.CreateEntryResponse]:
        # if not self.entry_is_open():
        #     logger.warning(f'Попытка записаться при закрытой записи пользователем {user_id}')
        #     raise LogicError('Запись закрыта')

        if len(data.selectedTimes) > config.common.max_entry_count:
            logger.warning(f'Попытка записаться больше {config.common.max_entry_count} раз на неделю пользователем {user_id}')
            raise LogicError(f'Максимальное число записей для одного пользователя - {config.common.max_entry_count} пользователем {user_id}')

        result: List[dto.CreateEntryResponse] = list()
        exist_avtime: List[AvailableTime] = list()
        with SessionCtx() as session:
            self.delete_old_entities(session, user_id)

            for selected_time in data.selectedTimes:
                avtime: AvailableTime | None = session.query(AvailableTime).get(selected_time)

                if avtime is None or avtime.deleted:
                    logger.warning(f'Попытка записаться на несуществующее время user.id={user_id}')
                    raise LogicError(f'Время с id={selected_time} не найдено')
                
                if avtime.month != get_next_month():
                    logger.warning(f'Попытка записаться не на следующий месяц user.id={user_id}')
                    raise LogicError(f'Вы можете записываться только на следующий месяц')
                
                if any(avtime.weekday == created_avtime.weekday for created_avtime in exist_avtime):
                    logger.warning(f'Попытка записаться на один день user.id={user_id}')
                    raise LogicError(f'На один день возможно записаться только единожды')
                
                exist_avtime.append(avtime)

                if session.query(Entry).where(
                    and_(
                        Entry.selected_time == selected_time,
                        Entry.deleted == False
                    )
                ).count() >= avtime.number_of_persons:
                    result.append(dto.CreateEntryResponse(
                        selectedTime=selected_time,
                        error=True,
                        text='Закончились места для записи'
                    ))
                    continue
                
                entry = Entry(
                    selected_time = selected_time,
                    user          = user_id
                )
                session.add(entry)
                session.flush((entry, ))

                result.append(dto.CreateEntryResponse(
                    selectedTime=selected_time,
                    error=False
                ))
                logger.success(f'Создана запись пользователем user.id={user_id} с entry.id={entry.id} на время available_time.id={selected_time}')
        
        return result
    

    def create(self, data: dto.EntryAddRequest) -> dto.GetEntryAnyResponse:
        with SessionCtx() as session:
            entry = Entry(
                selected_time = data.selectedTime,
                user          = data.user
            )
            session.add(entry)
            logger.success(f'Создана запись entry.id={entry.id} на время available_time.id={entry.selected_time}')
            return dto.GetEntryAnyResponse.from_orm(entry)


    def get_for_user(self, user_id: int, month: str = None)-> dto.GetEntryForUserResponse:
        if month is None:
            month = get_current_month()

        with SessionCtx() as session:
            return [
                dto.GetEntryForUserResponse.from_orm(entry)
                for entry in session.query(Entry)
                    .where(
                        and_(
                            Entry.deleted == False,
                            Entry.user == user_id,
                            AvailableTime.month == month
                        )
                    )
                    .join(Entry.available_time)
                    .order_by(Entry.id)
                    .all()
            ]


    def get(self, weekday: int = None, get_deleted = False) -> List[dto.GetEntryAnyResponse]:
        _filter = True

        if weekday is not None:
            _filter = and_(_filter, AvailableTime.weekday == weekday)
        
        if not get_deleted:
            _filter = and_(_filter, Entry.deleted == False)

        with SessionCtx() as session:
            return [
                dto.GetEntryAnyResponse.from_orm(entry)
                for entry in session.query(Entry).where(_filter).all()
            ]

    def delete(self, id: int, user_id: int, delete_any: bool = False):
        with SessionCtx() as session:
            entry: Entry | None = session.query(Entry).get(id)
            if entry is None or entry.deleted or (not delete_any and entry.user != user_id):
                raise DataBaseException('Запись не найдена')
            
            entry.deleted = True
            session.commit()

        logger.success(f'Удалена запись id={id} пользователем user.id={user_id}')

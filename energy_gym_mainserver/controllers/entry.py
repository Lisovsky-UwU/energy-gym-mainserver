from typing import Type
from typing import Dict
from typing import Tuple
from typing import Union
from typing import Iterable
from loguru import logger

from . import AvailableTimeDBController
from ..configmodule import config
from ..exceptions import LogicError
from ..services import EntryDBService
from ..models import dto
from ..orm import Entry


class EntryDBController:

    _entry_is_open = False


    @property
    @classmethod
    def entry_is_open(cls) -> bool:
        return cls._entry_is_open


    @classmethod
    def change_entry_open(cls, status: bool):
        cls._entry_is_open = status
        if cls._entry_is_open: logger.success('Запись открыта')
        else: logger.success('Запись закрыта')


    def __init__(
        self, 
        entry_service_type: Type[EntryDBService],
        avtime_controller: AvailableTimeDBController
    ):
        self.service_type = entry_service_type
        self.avtime_controller = avtime_controller


    def get_any(
        self,
        av_times: Union[Iterable[int], int] = (),
        users: Union[Iterable[int], int] = (),
        deleted: bool = False,
        **kwargs
    ) -> Tuple[dto.EntryModelExtended]:
        if isinstance(av_times, int):
            av_times = [av_times]

        if isinstance(users, int):
            users = [users]

        with self.service_type() as service:
            return self.__to_tuple_extended_model__(
                service.get_for_filter(
                    av_times = av_times,
                    users    = users,
                    deleted  = deleted
                )
            )
    
    
    def get_for_user(self, user_id: int) -> Tuple[dto.EntryModel]:
        with self.service_type() as service:
            return self.__to_tuple_model__(service.get_for_user(user_id))


    def create_by_user(self, user_id: int, selected_times_id: Iterable[int]) -> Tuple[dto.EntryModel]:
        if not self.entry_is_open:
            logger.info(f'Попытка записаться при закрытой записи пользователем {user_id}')
            raise LogicError('Запись закрыта')

        if len(selected_times_id) > config.common.max_entry_count:
            logger.info(f'Попытка записаться больще {config.common.max_entry_count} раз на неделю пользователем {user_id}')
            raise LogicError(f'Максимальное число записей для одного пользователя - {config.common.max_entry_count} пользователем {user_id}')
        
        with self.service_type() as entry_service:
            try:
                self.avtime_controller.check_create_for_id_list(selected_times_id)
            except Exception as e:
                logger.info(f'Ошибка при проверке записей для пользователя {user_id}: {e}')
                raise

            entry_list = entry_service.get_for_user(user_id)
            if len(entry_list) > 0:
                entry_service.delete_for_list(entry_list)

            entry_list = entry_service.create_for_iter(
                Entry(
                    selected_time = selected_time,
                    user          = user_id
                )
                for selected_time in selected_times_id
            )
            entry_service.commit()
            logger.trace(f'Созданы записи для пользователя с ID {user_id} на времена {selected_times_id} ({list(entry.id for entry in entry_list)})')

            return self.__to_tuple_model__(entry_list)


    def create(self, payload: Iterable[dto.EntryAddRequest]) -> Tuple[dto.EntryModel]:
        with self.service_type() as service:
            entry_list = service.create_for_iter(
                [
                    Entry(**entry.dict())
                    for entry in payload
                ]
            )
            service.commit()

            logger.trace(f'Созданы записи {list(entry.id for entry in entry_list)}')
            return self.__to_tuple_model__(entry_list)


    def delete(self, id_list: Iterable[int], user_id: int, delete_any: bool = False) -> Dict[int, str]:
        with self.service_type() as service:
            result_dict = dict()

            for entry_id in id_list:
                entry = service.get_by_id(entry_id)

                if entry is None or entry.deleted or (not delete_any and entry.user != user_id):
                    result_dict[entry_id] = 'Запись не найдена'

                else:
                    service.delete(entry, flush=True)
                    result_dict[entry_id] = 'Успешно'
            
            logger.trace(f'Удаление записей: {result_dict}')
            service.commit()
            return result_dict


    def from_orm_to_model(self, _from: Entry) -> dto.EntryModel:
        return dto.EntryModel(
            id            = _from.id,
            create_time   = _from.create_time,
            selected_time = self.avtime_controller.from_orm_to_model(_from.available_time),
            user          = _from.users,
        )


    def from_orm_to_extended_model(self, _from: Entry) -> dto.EntryModel:
        return dto.EntryModelExtended(
            id            = _from.id,
            create_time   = _from.create_time,
            selected_time = self.avtime_controller.from_orm_to_extended_model(_from.available_time),
            user          = _from.users,
            deleted       = _from.deleted,
        )


    def __to_tuple_model__(self, data: Iterable[Entry]) -> Tuple[dto.EntryModel]:
        return tuple(
            self.from_orm_to_model(entry)
            for entry in data
        )
    

    def __to_tuple_extended_model__(self, data: Iterable[Entry]) -> Tuple[dto.EntryModelExtended]:
        return tuple(
            self.from_orm_to_extended_model(entry)
            for entry in data
        )

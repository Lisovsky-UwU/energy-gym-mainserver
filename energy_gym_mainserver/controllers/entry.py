from typing import Type
from typing import Dict
from typing import Tuple
from typing import Union
from typing import Optional
from typing import Iterable

from . import AvailableTimeDBController
from ..configmodule import config
from ..exceptions import LogicError
from ..services import EntryDBService
from ..models import dto
from ..orm import Entry


class EntryDBController:

    entry_is_open = False

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


    def create(self, payload: dto.EntryAddRequest):
        with self.service_type() as service:
            entry = service.create(
                Entry(**payload.dict())
            )
            service.commit()

            return self.from_orm_to_model(entry)


    def create_by_user(self, user_id: int, selected_times_id: Iterable[int]) -> Tuple[dto.EntryModel]:
        if not self.entry_is_open:
            raise LogicError('Запись закрыта')

        if len(selected_times_id) > config.common.max_entry_count:
            raise LogicError(f'Максимальное число записей для одного пользователя - {config.common.max_entry_count}')
        
        with self.service_type() as entry_service:
            self.avtime_controller.check_create_for_id_list(selected_times_id)

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

            return self.__to_tuple_model__(entry_list)


    def create(self, payload: Iterable[dto.EntryAddRequest]) -> Tuple[dto.EntryModel]:
        with self.service_type() as service:
            entry_list = service.create_for_iter(
                [
                    Entry(**entry.dict())
                    for entry in payload.data
                ]
            )
            service.commit()

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

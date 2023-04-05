from typing import Type
from typing import List
from typing import Optional
from typing import Iterable

from . import AvailableTimeDBController
from ..configmodule import config
from ..exceptions import LogicError
from ..services import EntryDBService
from ..models import dto
from ..orm import Entry


class EntryDBController:

    def __init__(
        self, 
        entry_service_type: Type[EntryDBService],
        avtime_controller: AvailableTimeDBController
    ):
        self.entry_service_type = entry_service_type
        self.avtime_controller = avtime_controller

    
    def get_all(self, get_deleted: Optional[bool] = False) -> dto.EntryList:
        with self.entry_service_type() as entry_service:
            return self.__to_list_model__(entry_service.get_all(get_deleted))
        
    
    def get_for_user(self, user_id: int) -> dto.EntryList:
        with self.entry_service_type() as service:
            return self.__to_list_model__(service.get_for_user(user_id))


    def get_for_avtime(self, avtime_id: int) -> dto.EntryList:
        with self.entry_service_type() as service:
            return self.__to_list_model__(service.get_for_av_time(avtime_id))


    def create(self, payload: dto.EntryAddRequest):
        with self.entry_service_type() as service:
            entry = service.create(
                Entry(**payload.dict())
            )
            service.commit()

            return self.from_orm_to_model(entry)


    def create_by_user(self, user_id: int, selected_times_id: List[int]) -> dto.EntryList:
        if len(selected_times_id) > config.common.max_entry_count:
            raise LogicError(f'Максимальное число записей для одного пользователя - {config.common.max_entry_count}')
        
        with self.entry_service_type() as entry_service:
            self.avtime_controller.check_create_for_id_list(selected_times_id)

            entry_list = entry_service.get_for_user(user_id)
            if len(entry_list) > 0:
                entry_service.delete_for_list(entry_list)

            entry_list = entry_service.create_for_list(
                [
                    Entry(
                        selected_time = selected_time,
                        user          = user_id
                    )
                    for selected_time in selected_times_id
                ]
            )
            entry_service.commit()

            return self.__to_list_model__(entry_list)


    def create_for_list(self, payload: dto.EntryAddList) -> dto.EntryList:
        with self.entry_service_type() as service:
            entry_list = service.create_for_list(
                [
                    Entry(**entry.dict())
                    for entry in payload.data
                ]
            )
            service.commit()

            return self.__to_list_model__(entry_list)


    def from_orm_to_model(self, _from: Entry) -> dto.EntryModel:
        return dto.EntryModel(
            id            = _from.id,
            create_time   = _from.create_time,
            selected_time = self.avtime_controller.from_orm_to_model(_from.available_time),
            user          = _from.users,
        )


    def __to_list_model__(self, data: Iterable[Entry]) -> dto.EntryList:
        return dto.EntryList( data = self.__to_models__(data) )
         
    
    def __to_models__(self, data: Iterable[Entry]) -> List[dto.EntryModel]:
        return [
            self.from_orm_to_model(entry)
            for entry in data
        ]

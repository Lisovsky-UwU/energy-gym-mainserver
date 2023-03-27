from typing import Type
from typing import List
from typing import Optional
from typing import Iterable

from .converter import DTOConverter
from ..services import EntryDBService
from ..services import AvailableTimeDBService
from ..services import UserDBService
from ..models import dto
from ..orm import Entry


class EntryDBController:

    def __init__(
        self, 
        entry_service_type: Type[EntryDBService], 
        avtime_service_type: Type[AvailableTimeDBService], 
        user_service_type: Type[UserDBService], 
        converter: DTOConverter
    ):
        self.entry_service_type = entry_service_type
        self.avtime_service_type = avtime_service_type
        self.user_service_type = user_service_type
        self.converter = converter

    
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
            service.create(
                Entry(**payload.dict())
            )
            service.commit()


    def create_for_list(self, payload: dto.EntryAddList):
        with self.entry_service_type() as service:
            service.create_for_list(
                [
                    Entry(**entry.dict())
                    for entry in payload.data
                ]
            )
            service.commit()


    def __to_list_model__(self, data: Iterable[Entry]) -> dto.EntryList:
        return dto.EntryList( data = self.__to_models__(data) )
         
    
    def __to_models__(self, data: Iterable[Entry]) -> List[dto.EntryModel]:
        with self.avtime_service_type() as avtime_service, \
            self.user_service_type() as user_service:
            return [
                self.converter.entry_to_model(
                    _from         = entry,
                    selected_time = avtime_service.get_by_id(entry.selected_time),
                    user          = user_service.get_by_id(entry.user),
                )
                for entry in data
            ]

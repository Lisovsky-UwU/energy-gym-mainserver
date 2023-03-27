from typing import Optional
from typing import Type

from .converter import DTOConverter
from ..services import AvailableTimeDBService
from ..services import EntryDBService
from ..models import dto


class AvailableTimeDBController:
    
    def __init__(
        self, 
        av_service_type: Type[AvailableTimeDBService], 
        entry_service_type: Type[EntryDBService],
        converter: DTOConverter
    ):
        self.av_service_type = av_service_type
        self.entry_service_type = entry_service_type
        self.converter = converter

    
    def get_all(self, all_months: Optional[bool] = False, get_deleted: Optional[bool] = False) -> dto.AvailableTimeList:
        with self.av_service_type() as av_service, self.entry_service_type() as entry_service:
            if all_months:
                av_times = av_service.get_all(get_deleted)
            else:
                av_times = av_service.get_for_current_month()
            
            return dto.AvailableTimeList(
                data = [
                    self.converter.avtime_to_model(
                        av_time,
                        av_time.number_of_persons - len(entry_service.get_for_av_time(av_time.id))
                    )
                    for av_time in av_times
                ]
            )

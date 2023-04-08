from typing import Optional
from typing import Iterable
from typing import Type
from typing import Tuple
from typing import Union

from ..exceptions import LogicError
from ..services import AvailableTimeDBService
from ..models import dto
from ..orm import AvailableTime


class AvailableTimeDBController:
    
    def __init__(self, av_service_type: Type[AvailableTimeDBService]):
        self.service_type = av_service_type


    def create(self, av_time_list: Iterable[dto.AvailableTimeAddRequest]) -> Tuple[dto.AvailableTimeModel]:
        with self.service_type() as service:
            av_times = service.create_for_iter(
                AvailableTime(**av_time.dict())
                for av_time in av_time_list
            )
            service.commit()

            return self.__to_tuple_model__(av_times)


    def get_all(self, all_months: Optional[bool] = False, get_deleted: Optional[bool] = False) -> Tuple[dto.AvailableTimeModel]:
        with self.service_type() as service:
            if all_months:
                av_times = service.get_all(get_deleted)
            else:
                av_times = service.get_for_current_month()
            
            return self.__to_tuple_model__(av_times)


    def get_any(
        self,
        months: Union[Iterable[str], str] = (),
        deleted: bool = False,
        **kwargs
    ) -> Tuple[dto.AvailableTimeModelExtended]:
        if isinstance(months, str):
            months = [months]

        with self.service_type() as service:
            return self.__to_tuple_extended_model__(
                service.get_for_filter(
                    months  = months,
                    deleted = deleted
                )
            )


    def from_orm_to_model(self, _from: AvailableTime) -> dto.AvailableTimeModel:
        result = dto.AvailableTimeModel.from_orm(_from)
        result.free_seats = _from.number_of_persons - len(_from.not_deleted_entries)
        return result
    

    def from_orm_to_extended_model(self, _from: AvailableTime) -> dto.AvailableTimeModelExtended:
        result = dto.AvailableTimeModelExtended.from_orm(_from)
        result.free_seats = _from.number_of_persons - len(_from.not_deleted_entries)
        return result


    def all_id_list_in_db(self, id_list: Iterable[int]) -> bool:
        with self.service_type() as service:
            return all( service.get_by_id(avtime_id) is not None for avtime_id in id_list )


    def check_create_for_id_list(self, id_list: Iterable[int]):
        '''Поднимет ошибку LogicError в случае несоответствия'''
        with self.service_type() as service:
            avtimes = tuple( service.get_by_id(avtime_id) for avtime_id in id_list )

            for avtime in avtimes:
                if avtime is None:
                    raise LogicError('Не найдено одно из доступных времен для записи')
                if avtime.number_of_persons - len(avtime.not_deleted_entries) <= 0:
                    raise LogicError('Отсутствуют места для записи на одно из времен')
                if len([ _avt for _avt in avtimes if _avt.weekday == avtime.weekday ]) > 1:
                    raise LogicError('Максимальное число записей на один день - 1')


    def __to_tuple_model__(self, data: Iterable[AvailableTime]) -> Tuple[dto.AvailableTimeModel]:
        return tuple(
            self.from_orm_to_model(av_time)
            for av_time in data
        )


    def __to_tuple_extended_model__(self, data: Iterable[AvailableTime]) -> Tuple[dto.AvailableTimeModelExtended]:
        return tuple(
            self.from_orm_to_extended_model(av_time)
            for av_time in data
        )

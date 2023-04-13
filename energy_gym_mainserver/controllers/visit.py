from typing import Type
from typing import Tuple
from typing import Union
from typing import Iterable
from loguru import logger

from . import EntryDBController
from ..services import VisitDBService
from ..models import dto
from ..orm import Visit


class VisitDBController:

    def __init__(self, service_type: Type[VisitDBService], entry_controller: EntryDBController):
        self.service_type = service_type
        self.entry_controller = entry_controller


    def create(self, payload: Iterable[dto.VisitCreateRequest]) -> Tuple[dto.VisitModel]:
        with self.service_type() as service:
            result = service.create_for_iter(
                Visit(**visit.dict())
                for visit in payload
            )
            service.commit()

            logger.trace(f'Были созданы отметки посещений: {list(visit.id for visit in result)}')
            return self.__to_tuple_model__(result)


    def get_any(
        self,
        av_times: Union[Iterable[int], int] = (),
        entries: Union[Iterable[int], int] = (),
        users: Union[Iterable[int], int] = (),
        deleted: bool = False,
        **kwargs
    ):
        if isinstance(av_times, int):
            av_times = [av_times]

        if isinstance(entries, int):
            entries = [entries]

        if isinstance(users, int):
            users = [users]

        with self.service_type() as service:
            return self.__to_tuple_extend_model__(
                service.get_for_filter(
                    av_times = av_times,
                    entries  = entries,
                    users    = users,
                    deleted  = deleted
                )
            )


    def update(self, data: Iterable[dto.VisitUpdateRequest]) -> Tuple[dto.VisitModel]:
        with self.service_type() as service:
            result_list = list()

            for new_data in data:
                visit = service.get_by_id(new_data.id)

                if visit is not None:
                    visit.mark = new_data.mark
                    result_list.append(service.update(visit))
            
            service.commit()

            logger.trace(f'Были обновлены отметки: {list(visit.dict() for visit in data)}')
            return self.__to_tuple_model__(result_list)


    def __to_tuple_model__(self, data: Iterable[Visit]) -> Tuple[dto.VisitModel]:
        return tuple(
            dto.VisitModel(
                id    = visit.id,
                date  = visit.date,
                entry = self.entry_controller.from_orm_to_model(visit.entries),
                mark  = visit.mark
            )
            for visit in data
        )
    

    def __to_tuple_extend_model__(self, data: Iterable[Visit]) -> Tuple[dto.VisitModelExtended]:
        return tuple(
            dto.VisitModelExtended(
                id      = visit.id,
                date    = visit.date,
                entry   = self.entry_controller.from_orm_to_extended_model(visit.entries),
                mark    = visit.mark,
                deleted = visit.deleted
            )
            for visit in data
        )

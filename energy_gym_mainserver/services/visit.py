from typing import List
from typing import Iterable
from sqlalchemy import and_
from sqlalchemy.orm import Query

from .abc import BaseService
from ..orm import Visit
from ..orm import Entry


class VisitDBService(BaseService[Visit]):
    
    @property
    def query(self) -> Query:
        return self.session.query(self.model).join(Entry)


    def get_for_filter(
        self,
        av_times: Iterable[int] = (),
        entries: Iterable[int] = (),
        users: Iterable[int] = (),
        deleted: bool = False
    ) -> List[Visit]:
        _filter = True

        if len(av_times) > 0:
            _filter = and_(_filter, Entry.selected_time.in_(av_times))

        if len(entries) > 0:
            _filter = and_(_filter, Visit.entry.in_(entries))

        if len(users) > 0:
            _filter = and_(_filter, Entry.user.in_(users))

        return self.get_filtered(_filter, deleted)

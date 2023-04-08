from typing import List
from typing import Iterable
from typing import Optional
from sqlalchemy import and_

from .abc import BaseService
from ..orm import Entry


class EntryDBService(BaseService[Entry]):
    
    def get_for_filter(
        self,
        av_times: Iterable[int] = (),
        users: Iterable[int] = (),
        deleted: bool = False
    ) -> List[Entry]:
        _filter = True

        if len(av_times) > 0:
            _filter = and_(_filter, Entry.selected_time.in_(av_times))

        if len(users) > 0:
            _filter = and_(_filter, Entry.user.in_(users))
        
        return self.get_filtered(_filter, deleted)


    def get_for_av_time(self, av_time_id: int, get_deleted: Optional[bool] = False) -> List[Entry]:
        return self.get_filtered( 
            Entry.selected_time == av_time_id,
            get_deleted=get_deleted
        )
    

    def get_for_user(self, user_id, get_deleted: Optional[bool] = False) -> List[Entry]:
        return self.get_filtered(
            Entry.user == user_id,
            get_deleted=get_deleted
        )

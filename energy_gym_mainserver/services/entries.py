from typing import Iterable
from typing import Optional

from .abc import BaseService
from ..orm import Entry


class EntriesService(BaseService[Entry]):
    
    def get_for_av_time(self, av_time_id: int, get_deleted: Optional[bool] = False) -> Iterable[Entry]:
        return self.get_filtered( 
            Entry.selected_time == av_time_id,
            get_deleted=get_deleted
        )
    

    def get_for_user(self, user_id, get_deleted: Optional[bool] = False) -> Iterable[Entry]:
        return self.get_filtered(
            Entry.user == user_id,
            get_deleted=get_deleted
        )

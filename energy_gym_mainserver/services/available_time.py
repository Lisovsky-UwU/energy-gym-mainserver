from typing import List
from typing import Iterable
from typing import Optional
from datetime import datetime

from .abc import BaseService
from ..orm import AvailableTime
from ..configmodule import config


class AvailableTimeDBService(BaseService[AvailableTime]):

    def get_for_filter(
        self,
        months: Iterable[str] = (),
        deleted: bool = False
    ) -> List[AvailableTime]:
        if len(months) > 0:
            return self.get_filtered(AvailableTime.month.in_(months), deleted)
        else:
            return self.get_all(deleted)

    
    def get_for_current_month(self, get_deleted: Optional[bool] = False) -> List[AvailableTime]:
        return self.get_filtered(
            AvailableTime.month == datetime.now().strftime(config.available_time.month_format),
            get_deleted = get_deleted
        )

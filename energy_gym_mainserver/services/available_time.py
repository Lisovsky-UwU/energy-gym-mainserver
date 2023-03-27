from typing import Iterable
from typing import Optional
from datetime import datetime

from .abc import BaseService
from ..orm import AvailableTime
from ..configmodule import config


class AvailableTimeService(BaseService[AvailableTime]):
    
    def get_for_current_month(self, get_deleted: Optional[bool] = False) -> Iterable[AvailableTime]:
        return self.get_filtered(
            AvailableTime.month == datetime.now().strftime(config.common.av_month_format),
            get_deleted = get_deleted
        )

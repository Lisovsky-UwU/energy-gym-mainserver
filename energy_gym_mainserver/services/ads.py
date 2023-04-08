from typing import Iterable
from typing import List

from .abc import BaseService
from ..orm import Ads


class AdsDBService(BaseService[Ads]):
    
    def get_for_filter(
        self,
        users: Iterable[int] = (),
        deleted: bool = False
    ) -> List[Ads]:
        if len(users) > 0:
            return self.get_filtered(Ads.user.in_(users), deleted)
        else:
            return self.get_all(get_deleted=deleted)

from typing import List
from typing import Iterable
from sqlalchemy import and_

from .abc import BaseService
from ..orm import User


class UserDBService(BaseService[User]):
    
    def get_for_filter(
        self,
        groups: Iterable[str] = (),
        roles: Iterable[str] = (),
        deleted: bool = False
    ) -> List[User]:
        _filter = True

        if len(groups) > 0:
            _filter = and_(_filter, User.group.in_(groups))
        
        if len(roles) > 0:
            _filter = and_(_filter, User.role.in_(roles))
        
        return self.get_filtered(_filter, deleted)

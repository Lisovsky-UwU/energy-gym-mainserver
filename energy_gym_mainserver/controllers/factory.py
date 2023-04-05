from .available_time import AvailableTimeDBController
from .entry import EntryDBController
from .user import UserDBController
from ..services import AvailableTimeDBService
from ..services import EntryDBService
from ..services import UserDBService


class ControllerFactory:

    @classmethod
    def avtime(cls) -> AvailableTimeDBController:
        return AvailableTimeDBController(
            AvailableTimeDBService
        )
    
    @classmethod
    def entry(cls) -> EntryDBController:
        return EntryDBController(
            EntryDBService,
            cls.avtime()
        )
    
    @classmethod
    def user(cls) -> UserDBController:
        return UserDBController(
            UserDBService
        )
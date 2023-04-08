from .available_time import AvailableTimeDBController
from .entry import EntryDBController
from .visit import VisitDBController
from .user import UserDBController
from .ads import AdsDBController
from ..services import AvailableTimeDBService
from ..services import EntryDBService
from ..services import VisitDBService
from ..services import UserDBService
from ..services import AdsDBService


class ControllerFactory:

    @classmethod
    def ads(cls) -> AdsDBController:
        return AdsDBController(
            AdsDBService
        )

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

    @classmethod
    def visit(cls) -> VisitDBController:
        return VisitDBController(
            VisitDBService,
            cls.entry()
        )

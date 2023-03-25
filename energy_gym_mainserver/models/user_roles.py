from enum import Enum

from .access_rights import AccesRights


class UserRole(Enum):
    
    STUDENT = [
        AccesRights.AVAILABLETIME.GET,
        AccesRights.ENTRY.ADD,
        AccesRights.ENTRY.GET,
        AccesRights.ENTRY.DELETE,
        AccesRights.USER.GET,
        AccesRights.USER.DELETE
    ]

    ADMIN = [
        *AccesRights.get_all_rights()
    ]

from typing import List


class AvailableTimeAccess:

    '''Права доступов для информации по дням для записи'''
    ADD     = 'available time add'
    GET     = 'available time get'
    DELETE  = 'available time delete'

    @classmethod
    def get_all_rights(cls) -> List:
        return [
            cls.ADD,
            cls.GET,
            cls.DELETE,
        ]


class UserAccess:

    '''Права доступов для информации по пользователям'''
    EDITANY = 'user edit any'
    ADD     = 'user add'
    GET     = 'user get'
    DELETE  = 'user delete'

    @classmethod
    def get_all_rights(cls) -> List:
        return [
            cls.EDITANY,
            cls.ADD,
            cls.GET,
            cls.DELETE,
        ]


class EntyAccess:
    '''Права доступов для информации по записям'''

    EDITANY = 'entry edit any'
    ADD     = 'entry add'
    GET     = 'entry get'
    DELETE  = 'entry delete'

    @classmethod
    def get_all_rights(cls) -> List:
        return [
            cls.EDITANY,
            cls.ADD,
            cls.GET,
            cls.DELETE,
        ]


class AccesRights:
    '''Права доступов для редактирования и получения данных'''

    AVAILABLETIME = AvailableTimeAccess
    USER          = UserAccess
    ENTRY         = EntyAccess

    @classmethod
    def get_all_rights(cls) -> List:
        return [
            *cls.AVAILABLETIME.get_all_rights(),
            *cls.USER.get_all_rights(),
            *cls.ENTRY.get_all_rights(),
        ]

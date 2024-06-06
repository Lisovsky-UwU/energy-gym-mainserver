from enum import Enum


class VisitMark:
    
    PASS       = 0 # Пропуск
    ATTENDED   = 1 # Присутствовал
    VALID_PASS = 2 # Пропуск по уважительной
    CANCELLED  = 3 # Занятие отменено
    # BLOCKED    = 4 # Пользователь заблокирован


class UserRole(Enum):

    STUDENT = 'STUDENT'
    COACH = 'COACH'
    ADMIN = 'ADMIN'
    BLOCKED = 'BLOCKED'

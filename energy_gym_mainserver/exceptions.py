class EnergyGymMainServerException(Exception):
    '''Базовое исключение сервера'''

class APIException(EnergyGymMainServerException):
    '''Исключение при ошибке взаимодействия с API'''
    status_code = 400


class InvalidRequestException(APIException):
    '''Исключение при неверном теле запроса'''


class DataBaseException(EnergyGymMainServerException):
    '''Исключение при при ошибке в работе с базой данных'''


class TokenException(APIException):
    '''Исключение при неверном токене или его отсутствии'''
    status_code = 401


class LogicError(APIException):
    '''Исключение при ошибке в логике запроса'''

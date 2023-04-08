# Пока что будет так, после сделаю как-нибудь по умному
# Каждое время для записи состоит из weektime, то есть время на недели для записи

from .dto import AvailableTimeAddRequest


def default_time_list_factory():
    __week_days__ = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
    __time__ = ['16:00', '17:30', '19:00', '20:30']

    __list__ = []
    for d in __week_days__:
        for t in __time__:
            __list__.append(
                AvailableTimeAddRequest(
                    weektime=f'{d} - {t}',
                    number_of_persons=12
                )
            )

    return __list__

from datetime import date

from .configmodule import config


def get_current_month() -> str:
    return date.today().strftime(config.available_time.month_format)


def get_next_month() -> str:
    result = date.today()
    try:
        result = result.replace(month=result.month + 1)
    except ValueError:
        result = result.replace(month=1, year=result.year + 1)

    return result.strftime(config.available_time.month_format)

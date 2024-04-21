from datetime import date
import hashlib

from .configmodule import config


PASS_SECRET = 'seKs8whzkKyKnkvVzNe9RVCTxIskXSE6Le5'


def get_current_month() -> str:
    return date.today().strftime(config.available_time.month_format)


def get_next_month() -> str:
    result = date.today()
    try:
        result = result.replace(month=result.month + 1)
    except ValueError:
        result = result.replace(month=1, year=result.year + 1)

    return result.strftime(config.available_time.month_format)


def generate_hash(payload: str) -> str:
    return hashlib.sha256(payload.encode()).hexdigest()


def generate_hid(student_card: int, password: str) -> str:
    return generate_hash(
        f'{PASS_SECRET}{student_card}{password}{PASS_SECRET}'
    )

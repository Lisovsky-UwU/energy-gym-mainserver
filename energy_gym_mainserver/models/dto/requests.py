from typing import Iterable
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field

from .common import UserModel


def get_current_month():
    cur_time = datetime.now()
    return f'{cur_time.month}-{cur_time.year}'


# ---> Common <---

class ItemDeleteRequest(BaseModel):
    code : int


class ItemGetByCodeRequest(BaseModel):
    code : int


# ---> Available Time <---

class AvailableTimeAddRequest(BaseModel):
    weektime            : str
    number_of_persons   : int
    month               : str = Field(default_factory=get_current_month)


class AvailableTimeListAddRequest(BaseModel):
    data : Iterable[AvailableTimeAddRequest]


# ---> Entries <---

class EntryAddRequest(BaseModel):
    selected_time : int
    user_code     : int


class EntryListInTimeRequest(BaseModel):
    available_time : int


class EntryListUserRequest(BaseModel):
    user_code : int


# ---> Users <---

class UserCreateRequest(BaseModel):
    data : UserModel

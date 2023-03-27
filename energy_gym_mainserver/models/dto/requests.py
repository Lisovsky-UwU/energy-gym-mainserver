from typing import Iterable
from typing import List
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field

from .common import UserModel


def get_current_month():
    cur_time = datetime.now()
    return f'{cur_time.month}-{cur_time.year}'


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
    user_id       : int


class EntryAddList(BaseModel):
    data : List[EntryAddRequest]


# ---> Users <---

class UserCreateRequest(BaseModel):
    data : UserModel

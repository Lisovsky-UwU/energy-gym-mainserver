from typing import Iterable
from typing import Optional
from typing import List
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field

from ...configmodule import config


def get_current_month():
    return datetime.now().strftime(config.common.av_month_format)


# ---> Available Time <---

class AvailableTimeAddRequest(BaseModel):
    weekday             : int
    time                : str
    number_of_persons   : int
    month               : str = Field(default_factory=get_current_month)


class AvailableTimeListAddRequest(BaseModel):
    data : Iterable[AvailableTimeAddRequest]


# ---> Entries <---

class EntryAddRequest(BaseModel):
    selected_time : int
    user          : int


class EntryAddList(BaseModel):
    data : List[EntryAddRequest]


# ---> Users <---

class UserCreateRequest(BaseModel):
    student_card : int
    name         : str
    group        : str
    password     : str
    role         : str


class UserDataUpdateRequest(BaseModel):
    name         : Optional[str]
    group        : Optional[str]
    password     : Optional[str]

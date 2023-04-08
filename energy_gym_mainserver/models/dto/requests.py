from typing import Optional
from pydantic import BaseModel
from pydantic import Field

from ...utils import get_next_month


# ---> Ads <---

class AdsUpdateRequest(BaseModel):
    id   : int
    body : str


# ---> Available Time <---

class AvailableTimeAddRequest(BaseModel):
    weekday             : int
    time                : str
    number_of_persons   : int
    month               : str = Field(default_factory=get_next_month)


# ---> Entries <---

class EntryAddRequest(BaseModel):
    selected_time : int
    user          : int


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


class UserAnyDataUpdateRequest(UserDataUpdateRequest):
    id : int

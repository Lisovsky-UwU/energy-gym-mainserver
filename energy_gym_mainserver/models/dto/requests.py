from typing import Optional
from pydantic import BaseModel
from pydantic import validator
from pydantic import Field
from datetime import datetime
from datetime import date

from .. import VisitMark
from ...utils import get_next_month
from ...configmodule import config


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


# ---> Visit <---

class VisitCreateRequest(BaseModel):
    date  : date
    entry : int
    mark  : int = VisitMark.PASS.value


    @validator('date', pre=True)
    def date_validate(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, config.common.date_format).date()

        return value

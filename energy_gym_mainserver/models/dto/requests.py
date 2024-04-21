from typing import Any, Optional, List, Type
from pydantic import BaseModel, validator, Field
from datetime import datetime, date

from .. import VisitMark
from ...utils import get_next_month
from ...configmodule import config


# ---> Common <---

class DeleteRequest(BaseModel):
    id : int


# ---> Ads <---

class AdsCreateRequest(BaseModel):
    body : str


class AdsUpdateRequest(BaseModel):
    id   : int
    body : str


# ---> Available Time <---

class AvailableTimeAddRequest(BaseModel):
    weekday         : int
    time            : str
    numberOfPersons : int
    month           : str = Field(default_factory=get_next_month)


# ---> Entries <---

class EntryAddByUserRequest(BaseModel):
    selectedTimes : List[int]


class EntryAddRequest(BaseModel):
    selectedTime : int
    user         : int


# ---> Users <---

class UserGetRequest(BaseModel):
    role : Optional[str]


class UserCreateRequest(BaseModel):
    studentCard : int
    firstname   : str
    secondname  : str
    surname     : str
    group       : str
    password    : str
    role        : str


class UserDataUpdateRequest(BaseModel):
    firstname    : Optional[str]
    secondname   : Optional[str]
    surname      : Optional[str]
    group        : Optional[str]


class UserPasswordUpdateRequest(BaseModel):
    oldPassword : str
    newPassword : str


class UserAnyDataUpdateRequest(UserDataUpdateRequest):
    id : int
    newPassword: Optional[str]


# ---> Visit <---

class VisitGetReqeust(BaseModel):
    date  : Optional[date]
    time  : Optional[str]
    month : Optional[str]


class VisitCreateRequest(BaseModel):
    date  : date
    entry : int
    mark  : int = VisitMark.PASS


    @validator('date', pre=True)
    def date_validate(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, config.common.date_format).date()

        return value


class VisitUpdateRequest(BaseModel):
    id   : int
    mark : int

from typing import Any, Optional
from pydantic import BaseModel
from enum import Enum
import datetime


# ---> Common <---

class SuccessResponse(BaseModel):
    result : bool = True


# ---> Ads <---

class AdsResponse(BaseModel):
    id         : int
    body       : str
    createTime : str


    @classmethod
    def from_orm(cls, obj: Any) -> 'AdsResponse':
        return AdsResponse(
            id=obj.id,
            body=obj.body,
            createTime=obj.create_time.strftime('%d.%m.%Y')
        )


# ---> Available time <---

class AvailableTimeBase(BaseModel):
    id      : int
    weekday : int
    time    : str
    month   : str

    @classmethod
    def from_orm(cls, obj: Any) -> 'AvailableTimeBase':
        return AvailableTimeBase(
            id        = obj.id,
            weekday   = obj.weekday,
            time      = obj.time,
            month     = obj.month
        )


class AvailableTimeResponse(AvailableTimeBase):
    available : bool

    @classmethod
    def from_orm(cls, obj: Any, calculate_available =True) -> 'AvailableTimeResponse':
        return AvailableTimeResponse(
            id        = obj.id,
            weekday   = obj.weekday,
            time      = obj.time,
            month     = obj.month,
            available = obj.number_of_persons - len(obj.not_deleted_entries) > 0 if calculate_available else True
        )


class AvailableTimeAnyResponse(AvailableTimeBase):
    numberOfPersons : int
    freeSeats       : int

    @classmethod
    def from_orm(cls, obj: Any) -> 'AvailableTimeAnyResponse':
        return AvailableTimeAnyResponse(
            id              = obj.id,
            weekday         = obj.weekday,
            time            = obj.time,
            month           = obj.month,
            numberOfPersons = obj.number_of_persons,
            freeSeats       = obj.number_of_persons - len(obj.not_deleted_entries)
        )


# ---> User <---

class UserBaseResponse(BaseModel):
    firstname   : str
    secondname  : str
    surname     : str
    group       : str
    studentCard : int
    role        : str
    image       : Optional[str] = None

    @classmethod
    def from_orm(cls, obj: Any) -> 'UserBaseResponse':
        return UserBaseResponse(
            firstname   = obj.firstname,
            secondname  = obj.secondname,
            surname     = obj.surname,
            group       = obj.group,
            studentCard = obj.student_card,
            role        = obj.role.name,
            image       = obj.image
        )


class UserResponse(UserBaseResponse):
    id : int

    @classmethod
    def from_orm(cls, obj: Any) -> 'UserResponse':
        return UserResponse(
            id          = obj.id,
            firstname   = obj.firstname,
            secondname  = obj.secondname,
            surname     = obj.surname,
            group       = obj.group,
            studentCard = obj.student_card,
            image       = obj.image,
            role        = obj.role.name if isinstance(obj.role, Enum) else obj.role
        )


# ---> Entry <---

class CreateEntryResponse(BaseModel):
    selectedTime : int
    error        : bool
    text         : Optional[str]


class GetEntryForUserResponse(BaseModel):
    id           : int
    selectedTime : AvailableTimeBase

    @classmethod
    def from_orm(cls, obj: Any) -> 'GetEntryForUserResponse':
        return GetEntryForUserResponse(
            id           = obj.id,
            selectedTime = AvailableTimeBase.from_orm(obj.available_time)
        )


class GetEntryAnyResponse(BaseModel):
    id           : int
    selectedTime : AvailableTimeBase
    user         : UserResponse

    @classmethod
    def from_orm(cls, obj: Any) -> 'GetEntryAnyResponse':
        return GetEntryAnyResponse(
            id           = obj.id,
            selectedTime = AvailableTimeBase.from_orm(obj.available_time),
            user         = UserResponse.from_orm(obj.user_model)
        )


class OpenEntryResponse(BaseModel):
    status     : bool
    openingDay : int


# ---> Entry <---

class GetVisitResponse(BaseModel):
    id    : int
    date  : datetime.date
    # entry : GetEntryForUserResponse
    user  : UserResponse
    mark  : int

    @classmethod
    def from_orm(cls, obj: Any) -> 'GetVisitResponse':
        return GetVisitResponse(
            id    = obj.id,
            date  = obj.date,
            # entry = GetEntryForUserResponse.from_orm(obj.entry_model),
            user  = UserResponse.from_orm(obj.entry_model.user_model),
            mark  = obj.mark
        )


# ---> New <---

class NewResponse(BaseModel):
    id         : int
    body       : str
    createTime : str


    @classmethod
    def from_orm(cls, obj: Any) -> 'NewResponse':
        return NewResponse(
            id=obj.id,
            body=obj.body,
            createTime=obj.create_time.strftime('%d.%m.%Y')
        )

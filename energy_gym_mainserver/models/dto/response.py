from typing import Any, Type, Optional
from pydantic import BaseModel
from datetime import datetime


# ---> Common <---

class SuccessResponse(BaseModel):
    result : bool = True


class InDevelopResponse(BaseModel):
    result : str = 'In develop...'


# ---> Ads <---

class AdsResponse(BaseModel):
    id         : int
    body       : str
    createTime : str


    @classmethod
    def from_orm(cls: Type['AdsResponse'], obj: Any) -> 'AdsResponse':
        return AdsResponse(
            id=obj.id,
            body=obj.body,
            createTime=obj.create_time.strftime('%d.%m.%Y')
        )


# ---> Available time <---

class AvailableTimeBase(BaseModel):
    id      : int
    weekday : int
    time    : int
    month   : str

    @classmethod
    def from_orm(cls: Type['AvailableTimeBase'], obj: Any) -> 'AvailableTimeBase':
        return AvailableTimeBase(
            id        = obj.id,
            weekday   = obj.weekday,
            time      = obj.time,
            month     = obj.month
        )


class AvailableTimeResponse(AvailableTimeBase):
    available : bool

    @classmethod
    def from_orm(cls: Type['AvailableTimeResponse'], obj: Any, calculate_available =True) -> 'AvailableTimeResponse':
        return AvailableTimeResponse(
            id        = obj.id,
            weekday   = obj.weekday,
            time      = obj.time,
            month     = obj.month,
            available = obj.number_of_persons - obj.not_deleted_entries > 0 if calculate_available else True
        )


class AvailableTimeAnyResponse(AvailableTimeBase):
    numberOfPersons : int
    freeSeats       : int

    @classmethod
    def from_orm(cls: Type['AvailableTimeAnyResponse'], obj: Any) -> 'AvailableTimeAnyResponse':
        return AvailableTimeAnyResponse(
            id              = obj.id,
            weekday         = obj.weekday,
            time            = obj.time,
            month           = obj.month,
            numberOfPersons = obj.number_of_persons,
            freeSeats       = obj.number_of_persons - obj.not_deleted_entries
        )


# ---> User <---

class UserResponse(BaseModel):
    id          : int
    firstname   : str
    secondname  : str
    surname     : str
    group       : str
    studentCard : int

    @classmethod
    def from_orm(cls: type['UserResponse'], obj: Any) -> 'UserResponse':
        return UserResponse(
            id          = obj.id,
            firstname   = obj.firstname,
            secondname  = obj.secondname,
            surname     = obj.surname,
            group       = obj.group,
            studentCard = obj.student_card,
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
    def from_orm(cls: Type['GetEntryForUserResponse'], obj: Any) -> 'GetEntryForUserResponse':
        return GetEntryForUserResponse(
            id           = obj.id,
            selectedTime = AvailableTimeBase.from_orm(obj.available_time)
        )


class GetEntryAnyResponse(BaseModel):
    id           : int
    selectedTime : AvailableTimeBase
    user         : UserResponse

    @classmethod
    def from_orm(cls: Type['GetEntryAnyResponse'], obj: Any) -> 'GetEntryAnyResponse':
        return GetEntryAnyResponse(
            id = obj.id,
            selectedTime = AvailableTimeBase.from_orm(obj.available_time),
            user = UserResponse.from_orm(obj.user_model)
        )


class OpenEntryResponse(BaseModel):
    status : bool

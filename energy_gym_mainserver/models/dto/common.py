from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from datetime import date


# ---> User <---

class UserModel(BaseModel):
    id           : Optional[int]
    name         : str
    group        : str
    student_card : int

UserModel.Config.orm_mode = True


class  UserModelExtended(UserModel):
    password : str
    role     : str
    deleted  : bool

UserModelExtended.Config.orm_mode = True



# ---> Ads <---

class AdsModel(BaseModel):
    id          : Optional[int]
    create_time : datetime
    body        : str

AdsModel.Config.orm_mode = True


class AdsModelExtended(AdsModel):
    user    : Optional[UserModelExtended]
    deleted : bool

AdsModelExtended.Config.orm_mode = True



# ---> Available time <---

class AvailableTimeModel(BaseModel):
    id                : Optional[int]
    weekday           : int
    time              : str
    number_of_persons : int
    free_seats        : Optional[int]
    month             : str

AvailableTimeModel.Config.orm_mode = True


class AvailableTimeModelExtended(AvailableTimeModel):
    deleted : bool

AvailableTimeModelExtended.Config.orm_mode = True



# ---> Entry <---

class EntryModel(BaseModel):
    id            : Optional[int]
    create_time   : datetime
    selected_time : Optional[AvailableTimeModel]
    user          : Optional[UserModel]

EntryModel.Config.orm_mode = True


class EntryModelExtended(EntryModel):
    selected_time : Optional[AvailableTimeModelExtended]
    user          : Optional[UserModelExtended]
    deleted       : bool

EntryModelExtended.Config.orm_mode = True



# ---> Visit <---

class VisitModel(BaseModel):
    id    : Optional[int]
    date  : date
    entry : EntryModel
    mark  : int

VisitModel.Config.orm_mode = True


class VisitModelExtended(VisitModel):
    deleted: bool

VisitModelExtended.Config.orm_mode = True

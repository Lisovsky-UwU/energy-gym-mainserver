from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    id           : Optional[int]
    name         : str
    group        : str
    student_card : int

UserModel.Config.orm_mode = True


class AvailableTimeModel(BaseModel):
    id                : Optional[int]
    weektime          : str
    number_of_persons : int
    free_seats        : Optional[int]
    month             : str

AvailableTimeModel.Config.orm_mode = True


class EntryModel(BaseModel):
    id            : Optional[int]
    create_time   : datetime
    selected_time : Optional[AvailableTimeModel]
    user          : Optional[UserModel]

EntryModel.Config.orm_mode = True

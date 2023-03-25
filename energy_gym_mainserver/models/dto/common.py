from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    code  : int
    name  : str
    group : str


class AvailableTimeModel(BaseModel):
    code              : int
    weektime          : str
    number_of_persons : int
    free_seats        : int
    month             : str


class EntryModel(BaseModel):
    code          : int
    create_time   : datetime
    selected_time : AvailableTimeModel
    user          : UserModel

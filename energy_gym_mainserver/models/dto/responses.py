from typing import List
from pydantic import BaseModel

from .common import AvailableTimeModel
from .common import EntryModel
from .common import UserModel


# ---> Common <---



# ---> Available Time <---

class AvailableTimeList(BaseModel):
    data : List[AvailableTimeModel]


# ---> Entries <---

class EntryList(BaseModel):
    data : List[EntryModel]


# ---> Users <---

class UserList(BaseModel):
    data : List[UserModel]
